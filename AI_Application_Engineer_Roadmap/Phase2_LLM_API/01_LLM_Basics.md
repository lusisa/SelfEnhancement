# Phase 2: 大模型认知与基础应用 (LLM Basics)

要用好大模型，必须先了解它的基本原理和边界。

## 1. 核心概念理解
作为应用层开发者，你不需要手写底层 Transformer 模型，但必须懂这些概念：

*   **Transformer 架构**：大模型的基石，主要是 Self-Attention (自注意力机制)，使得模型能看到上下文并推断下一个 Token。
*   **Token**：大模型的最小处理单元，一个单词可能被切成多个 Token。无论是计费还是模型的 Context Window，都是以 Token 计量的。
*   **Context Window (上下文窗口)**：模型一次能接收和输出的最大 Token 数量 (例如 GPT-4 的 128K, Claude 3 的 200K)。理解这点对构建长文档 RAG 系统至关重要。
*   **Temperature (温度)**：控制输出的随机性。
    *   `0.0`: 确定性最强，适合代码生成、信息抽取、严格按照指令执行的场景。
    *   `0.7 - 1.0`: 创造力强，适合写文章、头脑风暴。
*   **Top-P (核采样)**：另一种控制随机性的参数，通常与 Temperature 选调其一。

## 2. API 参数与成本控制

在调用商业大模型时，注意以下几点：
*   **Prompt Tokens**：你发送给模型的提示词 Token 数量，较便宜。
*   **Completion Tokens**：模型生成的回复 Token 数量，通常比 Prompt Tokens 贵几倍。
*   **流式输出 (Streaming)**：就像 ChatGPT 打字一样的效果。使用服务器推送事件 (Server-Sent Events, SSE) 实现，这对提升用户体验极其关键。

## 3. 面试中常问的原理题

1.  "大模型为什么会出现幻觉 (Hallucination)？"
    *   本质是基于概率的下一个词预测，缺乏事实校验机制。
2.  "如何解决模型输入超过上下文限制的问题？"
    *   引入 RAG (检索增强生成)，只喂给模型相关的片段；或者使用长上下文窗口模型 (Long-context LLMs)。
