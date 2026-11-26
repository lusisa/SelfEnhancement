# 微调模型入门：情感分类 Demo

这是「微调一个预训练模型」的最小完整示例：把一个 **DistilBERT** 微调成
**影评正/负面分类器**。它跑通了微调的完整流程，这套思路对 LLM 和图像模型通用。

## 结果

- 数据：IMDB 影评，2000 条训练 + 500 条验证（全量 5 万条）
- 模型：`distilbert-base-uncased`（66M 参数）
- 训练：1 epoch，CPU，约 6 分钟
- **验证集准确率：86.2%**

## 如何运行

```bash
# 1. 创建虚拟环境并安装依赖（首次）
python3.13 -m venv venv
./venv/bin/pip install torch transformers datasets accelerate evaluate

# 2. 运行微调
./venv/bin/python finetune_sentiment.py
```

脚本开头会自动处理两件事（国内网络）：
- `HF_ENDPOINT=https://hf-mirror.com`（Hugging Face 镜像，可覆盖）
- `HF_HOME=./.hf_home`（缓存放项目内，不写 home 目录）

模型保存在 `output/sentiment-distilbert/`，含权重、tokenizer、配置。

## 这个 demo 教会你的微调通用流程

1. **加载预训练底座模型**（backbone）：`AutoModelForSequenceClassification.from_pretrained`
2. **换输出头**：`num_labels=2` 把原始输出头换成二分类头（新头是随机初始化的）
3. **用 tokenizer 把文本转成数字**：`truncation + padding`
4. **用自己的数据继续训练**（微调）
5. **评估 + 保存 + 推理**

日志里的 `LOAD REPORT` 很值得一看：
- `MISSING` = 新换上的分类头（预训练模型里没有，随机初始化，靠微调来训练）
- `UNEXPECTED` = 底座模型的语言理解部分（保留预训练权重，继续微调）

## 建议你亲手做的实验（这是最好的学习方式）

改 `finetune_sentiment.py` 顶部的 `CONFIG`，观察结果变化：

| 改什么 | 预期现象 | 学到什么 |
|---|---|---|
| `num_epochs` 1 → 3 | 准确率上升，但训练时间×3 | epoch 与欠拟合/过拟合 |
| `learning_rate` 2e-5 → 1e-3 | loss 震荡不收敛甚至炸 | 学习率太大不行 |
| `learning_rate` 2e-5 → 1e-6 | 收敛很慢 | 学习率太小也不行 |
| `train_size` 2000 → 10000 | 准确率更高 | 数据越多越好 |
| `model_name` → `bert-base-uncased` | 更慢但可能更准 | 模型越大能力越强、代价越高 |

## 下一步进阶路线

1. **LoRA/QLoRA 微调 LLM**（如 Qwen、LLaMA）：不训练全部权重，只训练一小部分，
   家用机也能微调大模型 → 见 Hugging Face `peft` 库。
2. **图像微调**：`AutoModelForImageClassification` + 你自己的图片数据集，
   流程和本 demo 几乎一模一样（换数据、换模型类）。
3. **从头训练小模型**：Karpathy《Let's build GPT》，彻底理解训练循环内部。
4. 大规模训练去 GPU 云：Colab 免费 T4、AutoDL、RunPod、云厂商实例。

## 学习资源

- Hugging Face 官方课程：https://huggingface.co/learn
- Andrej Karpathy《Neural Networks: Zero to Hero》
- 李宏毅《机器学习》（B站/YouTube）
- 《动手学深度学习》d2l.ai（中文版）
