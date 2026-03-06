---
name: AI Application Engineer Roadmap
overview: 一份为期6个月以上的系统性学习路线图，帮助你从Python初学者成长为能够胜任车企高级AI应用开发工程师的角色，涵盖大模型基础、RAG、Agent开发以及企业级系统集成。
todos:
  - id: phase_1_python
    content: "Phase 1: 深入学习 Python 面向对象编程、常用数据结构算法及 FastAPI 后端开发"
    status: completed
  - id: phase_2_llm_api
    content: "Phase 2: 掌握 LLM 基础概念、Prompt Engineering 以及大模型 API 的调用与集成"
    status: completed
  - id: phase_3_rag_agent
    content: "Phase 3: 熟练使用 LangChain/LlamaIndex，构建向量数据库并打通 RAG 与 Agent 开发全流程"
    status: completed
  - id: phase_4_projects
    content: "Phase 4: 了解车企研发流程(PLM/ERP)，并完成两个企业级的 AI 实战项目(RAG知识库 + 自动化Agent)"
    status: completed
  - id: phase_5_interview
    content: "Phase 5: 优化个人简历，重点突显业务场景深度集成能力，进行技术面试冲刺准备"
    status: completed
isProject: false
---

# 车企AI应用开发工程师：6个月+进阶学习计划

鉴于您目前处于**Python初学者**阶段，且**AI与车企领域知识为零**，而该岗位要求较高（4年以上经验、精通架构和流行AI框架），我们需要采取**“目标导向 + 高强度的项目实战”**策略，利用3-6个月以上的时间完成蜕变。以下为您量身定制的学习计划与能力图谱。

## 🎯 核心能力模型拆解（你需要掌握什么？）

1. **底层工程能力**：Python高阶语法、数据结构与算法、设计模式、后端开发基础（FastAPI/Flask）、Git版本控制。
2. **大模型核心技术**：Prompt Engineering、OpenAI等主流API调用、RAG（检索增强生成）全链路。
3. **AI框架与基础设施**：深入LangChain、LlamaIndex；熟练掌握向量数据库（Chroma, Milvus等）；了解PyTorch基础。
4. **Agent（智能体）开发**：多Agent协同（如AutoGen, LangGraph），让大模型学会使用工具（Tool Calling / Function Calling）。
5. **车企领域与业务集成**：熟悉PLM（产品生命周期管理）、ERP概念；能够设计AI系统与现有业务软件交互的架构。

---

## 📅 分阶段学习路线图（推荐 6 - 8 个月）

### 阶段一：夯实编程与工程化基础（1 - 1.5个月）

**目标**：达到能手写后端API，熟练处理数据的水平。

- **Python进阶**：吃透面向对象编程（OOP）、多线程/协程、装饰器。
- **数据结构与算法**：重点掌握数组、链表、树、哈希表，每天刷 1-2 道 LeetCode 简单/中等题培养逻辑。
- **软件工程实践**：学习常用的设计模式（单例、工厂、策略、观察者模式）；掌握 FastAPI 框架，能写出符合 RESTful 规范的接口。

### 阶段二：大模型认知与基础应用（第 1.5 - 2.5 个月）

**目标**：掌握让大模型输出预期结果的能力。

- **LLM原理普及**：了解 Transformer 架构基础，理解 Token、Context Window、Temperature 等核心概念。
- **Prompt Engineering**：系统学习结构化提示词编写，掌握 Few-shot prompting、CoT（思维链）等高级技巧。
- **API 实战**：注册并调用 OpenAI / 智谱 / 百度千帆 API，完成一个基于终端的多轮对话机器人。

### 阶段三：RAG、Agent与核心框架（第 2.5 - 4.5 个月）⭐ 核心阶段

**目标**：达到 JD 中要求的“深入理解主流大模型开发框架”。

- **RAG架构体系**：
  - 数据处理：文档解析、文本切分策略（Chunking）、数据清洗。
  - 向量检索：掌握 Embedding 模型的使用，学习向量数据库（如 Milvus / Qdrant）的部署与增删改查。
  - 高阶RAG优化：学习重排（Rerank）、查询改写（Query Transformation）。
- **核心框架精通**：
  - **LangChain & LlamaIndex**：不用只看文档，重点阅读这俩框架中 Retriever、Chain、Agent 模块的源码。
- **Agent开发**：掌握 ReAct 范式，利用 LangChain 的 Tool/Toolkit 让 LLM 能联网搜索、执行代码、查询本地数据库。

### 阶段四：业务场景模拟与企业级实战项目（第 4.5 - 6 个月）

**目标**：弥补行业经验不足，在简历中呈现“大型研发机构的场景深度集成”。

- **领域知识补充**：查阅资料了解车企研发 V 模型（需求-设计-实现-测试）；了解常见的车企软件（如西门子 Teamcenter PLM, SAP ERP）。
- **杀手锏项目 A（数据资产利用）**：**基于车企研发知识图谱/文档库的复杂 RAG 系统**。模拟几百份汽车零部件设计规范 PDF，做一个极低幻觉的问答系统，涉及混合检索（Hybrid Search）。
- **杀手锏项目 B（业务系统集成）**：**研发流程自动化 Agent 平台**。用 FastAPI 模拟一套 PLM 系统的查数据的接口，写一个 Agent，通过对话的方式让 AI 去你的接口抓数据、分析并自动生成测试报告。

---

## 💡 高效学习方法与求职策略

1. **项目驱动（Learning by Doing）**：岗位要求“开发自动化工具”、“全生命周期管理”。你学完每个知识点后，立刻变成 GitHub 上的一个开源小项目，不要只记笔记。
2. **拥抱 AI 导师**：遇到看不懂的算法、跑不通的报错、复杂的专业名词（如“仿真”、“PLM”），立刻向 Cursor / ChatGPT 提问。
3. **包装非技术背景**：JD 要求 4 年以上经验。如果您过往有其他行业经验（如项目管理、传统IT实施、咨询等），在写简历时需要将过去的经验与目前的 AI 技能**结合**，包装成“懂得业务痛点，且能用 AI 解决问题的跨界复合人才”。
4. **阅读前沿文献**：针对 JD 中的“优秀的英文读写能力”，建议每周阅读一篇知名的 AI 论文（如 ReAct, Plan-and-Solve）或大厂 AI 技术博客，保持对前沿技术的敏感度。

