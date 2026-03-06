# Phase 3: Agent 与 ReAct 范式

Agent (智能体) 是大语言模型从"回答问题"走向"解决问题"的里程碑。
在车企 AI 应用开发中，Agent 是让你实现"业务系统深度集成"和"开发自动化工具"的核心。

## 1. 什么是 Agent？
传统的 LLM 是闭门造车的静态大脑，不知道今天的日期，也无法操作你的电脑。
Agent 架构赋予了大模型 **工具 (Tools)** 的能力。

当用户提出一个复杂需求时，Agent 会：
1.  **思考 (Thought)**：我应该怎么做？
2.  **行动 (Action)**：我需要调用什么工具？（如：网络搜索工具、计算器、执行 SQL 查询 ERP 数据库的工具）
3.  **观察 (Observation)**：工具返回了什么结果？
然后根据观察结果继续思考，直到得出最终答案。

## 2. ReAct 范式 (Reasoning + Acting)
ReAct 是 Agent 最经典的基础运行逻辑。它的核心在于通过 Prompt 强迫模型遵循 "思考-行动-观察" 的循环。

**ReAct 的伪代码流程模型：**
```text
System Prompt: 
你有以下工具可用：
- search_web: 搜索互联网
- query_db: 查询 PLM 数据库

用户问题: "查一下底盘零件 BM101 的设计负责人是谁？"

=== Agent 运行日志 ===
Thought: 用户想知道 BM101 的负责人，我是一个大模型，我不知道内部数据。但我可以使用 query_db 工具去查。
Action: query_db
Action Input: "SELECT owner FROM parts WHERE part_id = 'BM101'"

Observation: {"owner": "张三(研发二部)"}

Thought: 我拿到了查询结果，我知道是谁了。
Final Answer: 底盘零件 BM101 的设计负责人是研发二部的张三。
```

## 3. Function Calling / Tool Calling
现在的模型（如 GPT-4, 智谱 GLM-4 等）在底层接口上原生支持了 Function Calling 机制，取代了纯文本层面的 ReAct 解析，使得 Agent 调用工具的成功率从 60% 飙升到了 95% 以上。

**学习重点**：
*   在 LangChain 中学习如何通过 `@tool` 装饰器定义自定义工具。
*   学习如何初始化一个 `create_tool_calling_agent` 和 `AgentExecutor`。
*   **进阶**：学习 LangGraph，通过图（节点与边）来编排极其复杂的多 Agent 协作流程。
