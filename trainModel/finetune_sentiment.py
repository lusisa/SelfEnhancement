# -*- coding: utf-8 -*-
"""
情感分类微调示例 —— 把 DistilBERT 微调成「影评正/负面」分类器
=============================================================

这是「微调一个预训练模型」的最小完整例子。虽然任务是文本分类，
但它覆盖了微调的通用流程，这套思路对 LLM 和图像模型完全一样：

    1. 加载一个「已经预训练好的底座模型」(pretrained backbone)
    2. 把它的输出头换成适合你任务的 (这里：二分类头)
    3. 用自己的数据继续训练它 (微调 fine-tuning)
    4. 评估 + 保存 + 用新模型推理

运行方式:
    python finetune_sentiment.py-
    环境变量 USE_MPS=0 可强制用 CPU--。

想真正理解每个词在干嘛，看下面每一-段注释。可调的超参数都集中在
最上面的「配置」区块里，改它们观察结果变化就是最好的学习方式。
"""

import os
import sys

# ---------------------------------------------------------------------
# 环境准备（必须在导入 datasets/transformers 之前执行）：
# 1. 国内网络默认走 hf-mirror.com 镜像（可用环境变量 HF_ENDPOINT 覆盖）；
# 2. 把 Hugging Face 缓存放到本项目目录下，避免写 home 目录、也便于清理。
# ---------------------------------------------------------------------
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
_HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("HF_HOME", os.path.join(_HERE, ".hf_home"))

import datasets
import evaluate
import numpy as np
import torch
import transformers

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

# =====================================================================
# 配置 —— 把所有可调的超参数集中在这里，方便你实验
# =====================================================================
CONFIG = {
    # 用哪个预训练模型。distilbert-base-uncased 只有 66M 参数，
    # 是 BERT 的「蒸馏版」，小、快、适合在普通电脑上练习。
    # 你可以换成 "bert-base-uncased"(110M)、"roberta-base" 等试试。
    "model_name": "distilbert-base-uncased",

    # 数据集：IMDB 影评，每条是一段英文评论 + 标签(0=负面, 1=正面)。
    # 全量有 5 万条，这里只取 2000 条训练 + 500 条验证，
    # 让第一次运行几分钟内跑完。想更认真就调大这些数字。
    "train_size": 2000,
    "eval_size": 500,

    # ---- 训练超参数（这是「训练模型」的核心可调项）----
    "learning_rate": 2e-5,   # 学习率：每一步更新权重的幅度。太大震荡、太小太慢
    "num_epochs": 1,         # 训练轮数：把整个训练集过几遍
    "per_device_train_batch_size": 16,  # 每步喂多少条样本。受内存限制
    "per_device_eval_batch_size": 32,
    "weight_decay": 0.01,    # 权重衰减：一种正则化，防止权重过大导致过拟合
    "warmup_ratio": 0.1,     # 前 10% 步线性升高学习率（warmup），训练更稳定

    "max_length": 256,       # 每条评论最多截断到多少个 token
    "output_dir": "output/sentiment-distilbert",  # 模型保存位置
}

# =====================================================================
# 0. 决定用 CPU 还是 Apple GPU (MPS)
# =====================================================================
def choose_device():
    """优先用 Apple Silicon 的 MPS 加速，失败则退回 CPU。"""
    if os.environ.get("USE_MPS", "1") == "0":
        return "cpu"
    try:
        if torch.backends.mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"


# =====================================================================
# 1. 加载数据集
# =====================================================================
def load_data(cfg):
    # datasets 库一行就能下载并加载公开数据集。
    # 注意：用「组织/名字」的完整仓库名（stanfordnlp/imdb），
    # 比简写 "imdb" 更稳，也避免某些版本下简写解析出错。
    raw = datasets.load_dataset("stanfordnlp/imdb")
    train = raw["train"].shuffle(seed=42).select(range(cfg["train_size"]))
    eval_ = raw["test"].shuffle(seed=42).select(range(cfg["eval_size"]))
    return train, eval_


# =====================================================================
# 2. 加载 tokenizer 和预训练模型
# =====================================================================
def load_model_and_tokenizer(cfg):
    # Tokenizer：把自然语言切成「token」并映射成数字 id。
    # 必须和预训练模型用同一个 tokenizer，否则模型看不懂输入。
    tokenizer = AutoTokenizer.from_pretrained(cfg["model_name"])

    # num_labels=2 表示「二分类」。
    # 这一步内部会：加载预训练权重 -> 把原本的输出头换成一个 2 分类头。
    # 换上去的新分类头是「随机初始化」的，微调就是在训练它 + 微调底层。
    model = AutoModelForSequenceClassification.from_pretrained(
        cfg["model_name"], num_labels=2
    )
    return model, tokenizer


# =====================================================================
# 3. 数据预处理：文本 -> 模型能吃的数字
# =====================================================================
def tokenize_fn(tokenizer, cfg):
    def _fn(example):
        return tokenizer(
            example["text"],
            truncation=True,          # 超过 max_length 就截断
            max_length=cfg["max_length"],
        )
    return _fn


# =====================================================================
# 4. 评估指标：准确率 accuracy
# =====================================================================
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)   # 输出 2 个 logits，取较大的那个为预测类别
    acc = (preds == labels).mean()
    return {"accuracy": acc}


# =====================================================================
# 5. 主流程
# =====================================================================
def main():
    cfg = CONFIG
    device = choose_device()
    print(f"[i] 使用设备: {device}")
    print(f"[i] PyTorch {torch.__version__} / transformers {transformers.__version__}")

    # ---- 数据 ----
    print("[i] 加载 IMDB 数据集...")
    train_ds, eval_ds = load_data(cfg)
    print(f"[i] 训练 {len(train_ds)} 条 / 验证 {len(eval_ds)} 条")

    # ---- 模型 ----
    print(f"[i] 加载模型 {cfg['model_name']} ...")
    model, tokenizer = load_model_and_tokenizer(cfg)

    # ---- 预处理 ----
    print("[i] 分词 tokenize...")
    train_ds = train_ds.map(tokenize_fn(tokenizer, cfg), batched=True)
    eval_ds = eval_ds.map(tokenize_fn(tokenizer, cfg), batched=True)
    # 保留模型需要的列，去掉多余字段
    keep = ["input_ids", "attention_mask", "label"]
    train_ds = train_ds.remove_columns(
        [c for c in train_ds.column_names if c not in keep]
    )
    eval_ds = eval_ds.remove_columns(
        [c for c in eval_ds.column_names if c not in keep]
    )
    train_ds.set_format("torch")
    eval_ds.set_format("torch")

    # ---- 训练参数 ----
    # warmup 步数：新版 transformers 用「步数」而不是「比例」，
    # 这里按训练集大小和 batch 换算成前 10% 的步数。
    total_steps = (len(train_ds) // cfg["per_device_train_batch_size"]) * cfg["num_epochs"]
    warmup_steps = int(total_steps * cfg["warmup_ratio"])

    training_args = TrainingArguments(
        output_dir=cfg["output_dir"],
        learning_rate=cfg["learning_rate"],
        num_train_epochs=cfg["num_epochs"],
        per_device_train_batch_size=cfg["per_device_train_batch_size"],
        per_device_eval_batch_size=cfg["per_device_eval_batch_size"],
        weight_decay=cfg["weight_decay"],
        warmup_steps=warmup_steps,
        eval_strategy="epoch",        # 每个 epoch 结束在验证集上评估一次
        save_strategy="epoch",        # 每个 epoch 保存一次 checkpoint
        logging_steps=10,             # 每 10 步打印一次 loss
        load_best_model_at_end=True,  # 训练完加载验证集上最好的那个 checkpoint
        metric_for_best_model="accuracy",
        seed=42,
        report_to=[],                 # 不接 wandb/tensorboard，保持简单
    )

    # data_collator：把不等长的样本动态 padding 成一批（batch）
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    # ---- 训练 ----
    print("[i] 开始微调训练...")
    trainer.train()

    # ---- 评估 ----
    print("[i] 在验证集上评估...")
    metrics = trainer.evaluate()
    print("[result] 验证集准确率 accuracy =", round(metrics["eval_accuracy"], 4))

    # ---- 保存最终模型 ----
    trainer.save_model(cfg["output_dir"])
    tokenizer.save_pretrained(cfg["output_dir"])
    print(f"[i] 模型已保存到 {cfg['output_dir']}")

    # ---- 推理演示：用微调后的模型判断几条新评论 ----
    print("\n===== 推理演示：给几条评论打分 =====")
    samples = [
        "This movie was fantastic! I loved every minute of it.",
        "Absolutely terrible. A complete waste of time and money.",
        "It was okay. Some parts were good but overall pretty average.",
    ]
    # 推理时用 eval 模式：关掉 dropout 等训练时才有的随机性
    model.eval()
    if device == "mps":
        model = model.to("mps")
    for s in samples:
        inputs = tokenizer(s, return_tensors="pt", truncation=True, max_length=cfg["max_length"])
        if device == "mps":
            inputs = {k: v.to("mps") for k, v in inputs.items()}
        with torch.no_grad():
            logits = model(**inputs).logits
        prob = torch.softmax(logits, dim=-1)[0]
        label = "正面 👍" if prob[1] > prob[0] else "负面 👎"
        print(f"  [{label}] (正面概率 {prob[1].item():.3f})  {s}")


if __name__ == "__main__":
    main()
