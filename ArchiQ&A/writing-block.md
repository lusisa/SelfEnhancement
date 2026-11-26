# 企业级多模态知识库 Agent 系统
## 技术设计与开发实施规范

**项目名称：** 建筑设计研究院企业级多模态知识库 Agent 系统  
**文档版本：** V1.0  
**项目类型：** 企业级 AI Agent / Multimodal RAG  
**部署方式：** 企业内网私有化部署  
**模型策略：** 本地模型 + 云端模型 API 混合调用  
**数据规模：** 中型，预计几万至几十万份文件  
**核心技术方向：** LLM、Agent、RAG、Multimodal AI、Agent Harness

---

# 第一章 项目概述

## 1.1 项目背景

某建筑设计研究院有限公司拥有大量企业内部知识资产，包括建筑设计文档、项目资料、技术规范、CAD 图纸、普通图片、历史问答记录、专家论坛内容以及其他业务系统中的结构化数据。

这些数据分散在不同的文件系统、业务数据库和知识平台中，存在以下问题：

1. 企业知识资产分散，员工难以快速查找所需资料。
2. 文档数量庞大，传统关键词搜索难以理解用户真实意图。
3. 文件夹具有多层嵌套结构，难以根据自然语言精准定位终极目录和文件。
4. Word、PDF、PPT、Excel、图片等数据格式不同，缺乏统一的知识处理机制。
5. 企业历史问答、专家论坛等碎片化知识难以有效利用。
6. 企业业务数据库中的结构化数据无法直接通过自然语言进行查询。
7. 普通图片需要具备视觉识别能力，并能够结合互联网公开信息进行补充分析。
8. CAD 等专业图纸不要求完整语义理解，但需要实现文件索引、图纸文字识别、精准检索和预览。

因此，需要建设一个基于大语言模型和 Agent 技术的企业级智能知识问答系统。

## 1.2 项目建设目标

建设一个支持多数据源、多文件格式、多模态理解、多路检索和多步骤任务执行的企业级 AI Agent 系统。

用户通过自然语言即可完成：

- 企业内部知识问答。
- 历史项目资料检索。
- 多层级文件夹和文件精准定位。
- 多文档联合检索和总结分析。
- 企业历史问答及专家经验检索。
- 结构化业务数据库查询。
- 普通图片识别和信息查询。
- CAD 图纸检索、文字识别和预览。
- 多步骤复杂任务规划和执行。

系统需要支持答案来源追溯，回答中尽可能提供对应文档、文件路径、页码、图纸和数据来源。

## 1.3 已确定的项目约束

| 项目 | 确定条件 |
|---|---|
| 部署环境 | 企业内网私有化部署 |
| 模型使用 | 本地模型 + 云端 API 混合 |
| 数据规模 | 几万到几十万份文件 |
| 原始数据 | 原则上保留在企业内网 |
| Agent 架构 | 多工具调用、工作流编排 |
| 知识库 | 多模态、异构数据统一管理 |
| CAD 理解 | 不要求专业语义理解 |
| 图片理解 | 普通实体物体识别及信息补充 |
| 回答要求 | 基于知识库证据回答，提供来源引用 |

云端模型调用必须经过数据安全策略检查，不允许默认将内部敏感资料上传到外部 API。

---

# 第二章 整体技术架构

## 2.1 系统架构设计

系统采用分层架构，主要包括：

1. 用户交互层。
2. 业务后端层。
3. Agent 编排层。
4. 模型网关层。
5. Agent Tools 工具层。
6. 多模态知识处理层。
7. 数据存储与检索层。
8. 基础设施层。

整体逻辑架构：

```text
                         用户
                          |
                          v
                  Web 前端交互系统
                          |
                          v
                  Java Spring Boot
                   业务后端服务
                          |
                    HTTP / SSE
                          |
                          v
                 Python FastAPI
                    Agent 服务
                          |
                          v
                  LangGraph Runtime
                          |
             +------------+------------+
             |            |            |
             v            v            v
          意图识别      任务规划      State管理
             |            |            |
             +------------+------------+
                          |
                          v
                  Agent Tool Router
                          |
       +------------------+------------------+
       |                  |                  |
       v                  v                  v
   Knowledge Tool     File Tool          SQL Tool
       |                  |                  |
       v                  v                  v
   RAG Retriever      文件目录检索        业务数据库
       |
       +------------------+------------------+
       |                  |                  |
       v                  v                  v
   Image Tool         CAD Tool           Web Search
       |                  |                  |
       v                  v                  v
      VLM               CAD索引            外部搜索
       |
       +------------------+------------------+
                          |
                          v
                    统一模型网关
                       LiteLLM
                          |
                 +--------+--------+
                 |                 |
                 v                 v
              本地模型           云端模型 API
                 |                 |
                 +--------+--------+
                          |
                          v
                     最终结果整合
                          |
                          v
                    答案及来源引用
                          |
                          v
                      用户展示
```

离线数据处理 Pipeline 独立运行：

```text
企业数据源
   |
   +-- 文件系统
   +-- Word / PDF / PPT / Excel
   +-- 普通图片
   +-- CAD 图纸
   +-- 历史问答
   +-- 专家论坛
   +-- 业务数据库
          |
          v
       数据采集层
          |
          v
       文件类型识别
          |
          v
       异步解析任务队列
          |
          v
       多模态解析器
          |
          +-- Word Parser
          +-- PDF Parser
          +-- PPT Parser
          +-- Excel Parser
          +-- Image Parser
          +-- CAD Parser
          +-- Q&A Parser
          +-- Database ETL
          |
          v
       数据标准化
          |
          v
       文本清洗与结构化
          |
          v
       Chunk 切片
          |
          v
       Embedding
          |
          v
       多路索引构建
          |
          +-- PostgreSQL
          +-- pgvector
          +-- Elasticsearch
          +-- MinIO
```

## 2.2 架构设计原则

### 原则一：数据处理和在线问答解耦

文件解析、OCR、Embedding 等任务属于计算密集型任务，不应该阻塞用户的在线问答请求。

采用消息队列实现异步处理。

### 原则二：Agent 不直接操作底层数据库

Agent 通过 Tool 调用业务能力。

例如：

```text
Agent
  |
  v
search_file Tool
  |
  v
FileService
  |
  v
PostgreSQL
```

Agent 不能直接获得任意 SQL 执行权限。

### 原则三：不同数据类型采用不同解析策略

不能将所有数据都转换为普通文本后进行向量化。

需要针对不同格式建立独立 Parser。

### 原则四：模型调用统一管理

所有本地模型和云端模型调用统一经过 Model Gateway。

### 原则五：模块化设计，避免初期过度微服务化

初期采用模块化单体架构和独立异步 Worker：

- Spring Boot 业务服务。
- FastAPI Agent 服务。
- Python 文档处理 Worker。
- 独立模型推理服务。
- 数据存储服务。

未来根据并发量、部署规模和团队分工再考虑拆分微服务。

---

# 第三章 技术选型

## 3.1 技术栈总览

| 分类 | 技术选型 | 主要职责 |
|---|---|---|
| 前端 | Vue 3 | 用户交互 |
| 业务后端 | Java Spring Boot | 用户、权限、文件管理、业务接口 |
| Agent 后端 | Python FastAPI | Agent 服务入口 |
| Agent 编排 | LangGraph | Agent 工作流及状态管理 |
| LLM 工具框架 | LangChain | 模型封装、Prompt、Retriever、Tools |
| 工具协议 | MCP | 标准化工具连接，可按需引入 |
| 本地模型部署 | vLLM | 大模型推理服务 |
| 模型网关 | LiteLLM | 统一模型调用和路由 |
| Embedding | BGE-M3 | 文本向量化 |
| Reranker | BGE Reranker | 检索结果重排序 |
| 文档解析 | Docling、Apache Tika | 文档解析 |
| Word/PPT/Excel | python-docx、python-pptx、openpyxl | Office 文件处理 |
| PDF | PyMuPDF | PDF 文本及页面处理 |
| OCR | PaddleOCR | 图片及扫描文件文字识别 |
| VLM | Qwen-VL 等 | 图片理解 |
| CAD | ODA SDK、ezdxf | CAD 文件解析 |
| 关系数据库 | PostgreSQL | 元数据、业务信息 |
| 向量检索 | pgvector | 向量检索 |
| 全文检索 | Elasticsearch | BM25 关键词检索 |
| 对象存储 | MinIO | 文件和解析产物 |
| 缓存 | Redis | 缓存、会话及状态 |
| 消息队列 | RabbitMQ | 异步任务 |
| 可观测性 | Langfuse | LLM 和 Agent 调用追踪 |
| 监控 | Prometheus + Grafana | 系统运行监控 |
| 部署 | Docker Compose | 初期容器化部署 |

以上是候选技术基线，实际实施时应根据硬件资源、许可证、模型兼容性和已有企业基础设施调整。

## 3.2 Java 和 Python 的职责边界

采用 Java + Python 双技术栈。

### Java Spring Boot

负责：

- 用户登录和身份认证。
- 用户、角色、部门管理。
- 企业权限管理。
- 文件上传和文件管理。
- 文件元数据管理接口。
- 知识库管理。
- 对话记录管理。
- Agent 服务调用。
- 文件预览和下载接口。
- 业务系统数据接入。

### Python FastAPI

负责：

- Agent 运行时。
- LangGraph 工作流。
- LLM 调用。
- Tool Calling。
- RAG 检索。
- 文档解析。
- Embedding。
- Reranker。
- OCR。
- VLM。
- SQL Agent Tool。
- Web Search Tool。
- Agent State 管理。

两个服务之间使用 HTTP API 通信。

长时间运行的任务通过 RabbitMQ 异步执行。

---

# 第四章 模型基础设施设计

## 4.1 混合模型部署

本项目需要同时支持本地模型和云端模型。

本地模型负责：

- 普通问答。
- 企业知识库问答。
- 敏感数据处理。
- Embedding。
- Reranker。
- 图片识别。
- 意图分类。

云端模型负责：

- 经授权的数据参与的复杂推理。
- 高复杂度任务。
- 特定情况下更高质量的视觉理解。
- 本地模型无法完成的任务。

具体模型根据 GPU 资源和业务测试确定。

建议优先评估：

- 本地 LLM：Qwen 系列。
- 本地 VLM：Qwen-VL 系列。
- Embedding：BGE-M3。
- Reranker：BGE Reranker。
- 推理框架：vLLM。
- 统一网关：LiteLLM。

## 4.2 Model Gateway

设计统一模型网关。

所有 Agent 和数据处理模块不得直接硬编码调用某一个模型厂商的 API。

统一调用接口：

```python
class ModelGateway:

    async def chat(
        self,
        messages,
        model_type="llm",
        task_type=None,
        data_level=None,
        **kwargs
    ):
        pass

    async def embedding(
        self,
        texts,
        **kwargs
    ):
        pass

    async def rerank(
        self,
        query,
        documents,
        **kwargs
    ):
        pass

    async def vision(
        self,
        image,
        prompt,
        **kwargs
    ):
        pass
```

以上为接口设计示意，具体可根据 LangChain Runnable、LiteLLM 等实现。

## 4.3 模型路由策略

根据任务类型和数据安全级别选择模型。

| 任务 | 默认模型 |
|---|---|
| 意图识别 | 本地小模型 |
| 普通问答 | 本地 LLM |
| 企业 RAG 问答 | 本地 LLM |
| 复杂推理 | 经安全审批的云端 LLM |
| 普通图片识别 | 本地 VLM |
| 复杂图片理解 | 经授权的云端 VLM |
| Embedding | 本地 Embedding |
| Reranker | 本地 Reranker |

建立数据分级：

- L1：公开数据。
- L2：内部一般数据。
- L3：敏感项目及业务数据。

L3 数据禁止传输至云端。

L2 数据默认本地处理，如需调用云端必须经过授权、脱敏和策略检查。

云端调用需要记录：

- 调用模型。
- 调用时间。
- 请求任务类型。
- 数据级别。
- 脱敏情况。
- 调用结果。
- Token 消耗。

---

# 第五章 数据存储设计

## 5.1 PostgreSQL

作为系统核心关系数据库，负责存储：

- 文件元数据。
- 文件夹目录关系。
- 文档解析状态。
- Chunk 元数据。
- 知识碎片。
- 用户和权限关联信息。
- 项目基础信息。
- Agent 会话及执行记录。
- 图纸元数据。

同时使用 pgvector 存储文本向量。

## 5.2 Elasticsearch

负责：

- 文件名称检索。
- 文件夹名称检索。
- 文件路径检索。
- 文件全文检索。
- 图纸名称检索。
- 图纸编号检索。
- BM25 关键词召回。

## 5.3 MinIO

负责存储：

- 原始 Word、PDF、PPT、Excel。
- 原始图片。
- CAD 文件。
- 文档解析后的图片。
- 图纸预览文件。
- 其他衍生文件。

原始文件必须保留，解析产物不能代替原始文件。

## 5.4 Redis

负责：

- Agent 会话缓存。
- 临时任务状态。
- 查询结果缓存。
- 热点数据缓存。
- 分布式锁。
- 短期任务状态。

需要持久化的 Agent Checkpoint 应采用可靠的持久化存储，不能只依赖 Redis 缓存。

## 5.5 RabbitMQ

负责：

- 文件解析任务。
- OCR 任务。
- VLM 识别任务。
- Embedding 任务。
- Elasticsearch 索引任务。
- 数据库同步任务。
- 文件更新及删除任务。

采用异步任务模式：

```text
文件上传
   |
   v
创建解析任务
   |
   v
RabbitMQ
   |
   v
Parser Worker
   |
   v
解析和清洗
   |
   v
Embedding Worker
   |
   v
索引构建
   |
   v
任务完成
```

要求：

1. 任务支持失败重试。
2. 任务具备幂等性。
3. 支持任务状态追踪。
4. 支持失败任务重新执行。
5. 支持死信队列。
6. 支持文档增量更新。

---

# 第六章 文件管理与多层级目录检索

这是本项目的核心业务能力之一。

## 6.1 目录树管理

采用 PostgreSQL 邻接表模型。

文件和目录统一存储在知识文件表中，通过 node_type 区分。

建议表结构：

### knowledge_node

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT | 主键 |
| parent_id | BIGINT | 父目录 ID |
| node_type | VARCHAR | DIRECTORY / FILE |
| name | VARCHAR | 名称 |
| file_type | VARCHAR | 文件类型 |
| full_path | TEXT | 完整路径 |
| storage_key | TEXT | MinIO 对象 Key |
| project_id | BIGINT | 所属项目 |
| content_hash | VARCHAR | 文件哈希 |
| file_size | BIGINT | 文件大小 |
| version | VARCHAR | 文件版本 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

要求：

- 目录和文件具有唯一 ID。
- 每个节点记录 parent_id。
- 保留完整路径。
- 支持多层级递归查询。
- 支持根据目录 ID 查找子节点。
- 支持根据文件 ID 获取完整路径。
- 支持目录移动时更新路径。
- 支持文件版本管理。
- 支持文件删除后的索引同步。

PostgreSQL 递归 CTE 用于获取祖先或后代目录。

向量检索不能替代目录树查询。

## 6.2 文件检索策略

文件检索采用多路方式：

1. 文件名称精确匹配。
2. 文件名称关键词匹配。
3. Elasticsearch BM25 检索。
4. 文件内容向量检索。
5. 目录路径检索。
6. 项目名称、专业分类等元数据过滤。

例如用户提问：

“帮我找一下上海某住宅项目的设计方案。”

Agent 执行：

```text
用户问题
   |
   v
提取项目名称和文件类型
   |
   v
search_file Tool
   |
   v
Elasticsearch + PostgreSQL
   |
   v
返回候选项目目录和文件
   |
   v
校验项目目录及文件关系
   |
   v
get_file_path Tool
   |
   v
返回真实完整路径
   |
   v
展示文件及预览
```

路径必须以数据库中的真实记录为准，禁止 LLM 自行生成文件路径。

---

# 第七章 多模态数据接入与解析

## 7.1 统一数据接入机制

所有数据源统一进入数据接入层。

数据接入层负责：

- 文件扫描。
- 文件上传。
- 文件类型识别。
- 文件哈希计算。
- 文件去重。
- 文件元数据登记。
- 解析任务创建。
- 任务状态跟踪。
- 增量同步。

建立统一 Parser 接口：

```python
from abc import ABC, abstractmethod

class BaseParser(ABC):

    @abstractmethod
    def supports(self, file_type: str) -> bool:
        pass

    @abstractmethod
    async def parse(self, file_info):
        pass
```

所有 Parser 返回统一的解析结果对象。

建议统一输出结构：

```json
{
  "file_id": 1001,
  "file_name": "建筑设计方案.docx",
  "file_type": "docx",
  "content": [],
  "metadata": {},
  "images": [],
  "tables": [],
  "pages": [],
  "status": "success"
}
```

实际实现需要根据文件类型保留相应的结构信息，不能要求每种文件都填充全部字段。

## 7.2 Word 解析

推荐 python-docx 或 Docling。

需要提取：

- 标题。
- 段落。
- 表格。
- 图片。
- 标题层级。
- 文档元数据。

保留章节层级，避免破坏文档上下文。

## 7.3 PDF 解析

推荐 Docling + PyMuPDF。

需要支持：

- 原生 PDF 文本提取。
- 页面编号。
- 标题层级。
- 表格提取。
- 图片提取。
- 扫描版 PDF OCR。
- 页面和文本块关联。

扫描版 PDF 需要通过 OCR 进行处理。

## 7.4 PPT 解析

推荐 python-pptx。

提取：

- 幻灯片编号。
- 标题。
- 文本框内容。
- 表格。
- 备注。
- 图片。

每张幻灯片应保留独立上下文，避免不同页面内容混淆。

## 7.5 Excel 解析

推荐 openpyxl。

提取：

- Sheet 名称。
- 行列结构。
- 表头。
- 单元格数据。
- 数据类型。
- 合并单元格。
- 表格范围。

Excel 不应直接按照普通长文本进行固定长度切片。

需要保留表格上下文。

对于需要精确统计、计算的内容，优先进入结构化数据库，通过 SQL Tool 查询。

## 7.6 普通图片解析

普通图片包括建筑实体、建筑工具、施工设备等。

处理流程：

```text
图片
 |
 v
图片预处理
 |
 v
OCR
 |
 v
VLM 图片理解
 |
 v
提取物体名称和关键属性
 |
 v
判断是否需要联网查询
 |
 v
Web Search Tool
 |
 v
获取外部公开信息
 |
 v
结合企业知识库和外部资料
 |
 v
生成回答
```

候选技术：

- PaddleOCR。
- Qwen-VL。
- CLIP / SigLIP（如有图片向量检索需求）。
- Web Search API。

YOLO 可以作为后续目标检测增强方案，不作为第一期必选依赖。

注意：

外部搜索结果需要进行来源验证，并与企业内部资料区分引用。

图片本身不应未经数据安全检查就上传至云端模型。

## 7.7 知识碎片解析

知识碎片包括：

- 历史用户问答。
- 专家论坛帖子。
- 专家讨论。
- 专业经验记录。

建立独立知识碎片数据模型。

### knowledge_fragment

| 字段 | 说明 |
|---|---|
| id | 知识 ID |
| source_type | USER_QA / EXPERT_POST |
| question | 原始问题 |
| answer | 原始回答 |
| content | 完整内容 |
| author | 作者 |
| category | 专业分类 |
| source_id | 来源系统记录 ID |
| created_at | 创建时间 |
| embedding | 向量 |

Question 和 Answer 必须保持关联。

检索时同时考虑问题语义、回答内容、专业分类和时间等信息。

## 7.8 CAD 专业图纸处理

第一期不实现 CAD 专业语义理解。

重点实现：

1. CAD 文件登记。
2. 文件名称识别。
3. 图纸编号识别。
4. DWG / DXF 文件文字提取。
5. 图层及基础实体信息提取（可选）。
6. 扫描版图纸 OCR。
7. 图纸元数据索引。
8. 原始图纸召回。
9. 图纸预览。

候选技术：

- ODA File Converter / ODA SDK。
- ezdxf。
- PaddleOCR。
- PDF / SVG / PNG 转换工具。
- Web CAD Viewer。

建议建立 CAD 专用数据表：

### cad_drawing

| 字段 | 说明 |
|---|---|
| id | 图纸 ID |
| file_id | 关联原始文件 |
| drawing_name | 图纸名称 |
| drawing_number | 图纸编号 |
| project_name | 项目名称 |
| drawing_type | 图纸类型 |
| extracted_text | 提取文字 |
| preview_key | 预览文件 Key |
| original_key | 原始文件 Key |
| created_at | 创建时间 |

用户要求展示图纸时，返回：

- 图纸名称。
- 图纸编号。
- 所属项目。
- 原始文件。
- 预览文件。
- 文件路径。

CAD 文件的展示必须经过权限校验。

---

# 第八章 RAG 检索系统

## 8.1 RAG 设计目标

建立支持多种检索方式的企业级 RAG 系统。

采用：

Hybrid Search + Metadata Filtering + Reranker + Context Assembly。

## 8.2 Chunk 切片策略

不能对所有文档使用统一固定长度切片。

根据数据类型采用不同策略：

| 文件类型 | 切片策略 |
|---|---|
| Word | 标题层级 + 段落 |
| PDF | 页面结构 + 标题 + 段落 |
| PPT | 每页独立切片 |
| Excel | Sheet + 表格 + 行列上下文 |
| 知识问答 | 问题与回答关联切片 |
| 专家帖子 | 帖子主体 + 评论关联 |
| 图片 | OCR 文本 + VLM 描述 |
| CAD | 文字信息及图纸元数据 |

对于较长文档，采用 Parent-Child Chunk 机制：

- Parent Chunk：保留完整章节上下文。
- Child Chunk：作为向量检索单元。

检索到 Child 后，可以根据需要获取 Parent 上下文。

每个 Chunk 必须关联：

- file_id。
- chunk_id。
- file_name。
- full_path。
- page_number。
- chapter。
- section。
- project_id。
- document_version。
- permission_scope。

## 8.3 Embedding

使用 BGE-M3 作为首选候选模型。

将文本转换为向量。

Embedding 需要统一版本管理：

- 模型名称。
- 模型版本。
- 向量维度。
- 文本预处理版本。
- 创建时间。

模型升级后需要考虑向量重建。

## 8.4 Hybrid Search

结合：

### Dense Vector Search

通过 pgvector 进行语义向量检索。

适合：

- 语义相似问题。
- 专业知识问答。
- 描述性内容检索。

### Sparse / BM25 Search

通过 Elasticsearch 进行关键词检索。

适合：

- 项目名称。
- 文件名称。
- 图纸编号。
- 国家标准编号。
- 人名。
- 专业术语。

### RRF

使用 Reciprocal Rank Fusion 融合多路检索结果。

### Reranker

对初步召回的候选结果进行相关性重排序。

## 8.5 推荐检索流程

```text
用户 Query
    |
    v
Query Understanding
    |
    v
Query Rewrite（必要时）
    |
    +---------------------+
    |                     |
    v                     v
BM25 检索              Vector 检索
    |                     |
    +----------+----------+
               |
               v
          RRF 融合
               |
               v
          Reranker
               |
               v
         权限二次校验
               |
               v
        Top-K Context
               |
               v
       Context Assembly
               |
               v
          LLM 回答
               |
               v
        来源引用及展示
```

注意：权限过滤必须在检索之前执行，权限二次校验不能替代前置权限过滤。

## 8.6 检索结果引用

每个检索结果必须保留来源信息。

例如：

```json
{
  "file_id": 1001,
  "file_name": "建筑设计方案.docx",
  "full_path": "/设计项目/商业建筑/项目A/建筑设计方案.docx",
  "page_number": 12,
  "chunk_id": "chunk_001",
  "content": "本项目采用...",
  "score": 0.92
}
```

最终回答应支持：

- 文件名称引用。
- 文件预览。
- 原文定位。
- PDF 页码定位。
- 图纸预览。
- 数据来源引用。

不能将模型自行生成的来源当成真实引用。

---

# 第九章 Agent 核心架构

## 9.1 Agent 设计目标

系统不能仅仅实现用户提问、向量检索、LLM 回答的简单 RAG 流程。

需要具备：

- 意图识别。
- 任务拆解。
- 工具选择。
- 多步骤执行。
- 执行结果判断。
- 必要时再次调用工具。
- 上下文管理。
- 错误处理。
- 最终回答整合。

采用 LangGraph 作为核心编排框架。

设计原则：

**确定性 Workflow + 局部 Agent 自主决策。**

不要将所有逻辑交给一个没有执行边界的无限循环 Agent。

## 9.2 Agent 工作流程

```text
用户问题
   |
   v
问题理解节点
   |
   v
意图分类节点
   |
   v
任务规划节点
   |
   v
条件路由节点
   |
   +-------------------------------+
   |           |          |        |
   v           v          v        v
 Knowledge   File       SQL      Image
   Tool      Tool       Tool      Tool
   |           |          |        |
   v           v          v        v
 RAG         目录检索    SQL      VLM
   |           |          |        |
   +-----------+----------+--------+
                    |
                    v
                 结果评估
                    |
             +------+------+
             |             |
             v             v
           不充分         充分
             |             |
             v             v
          补充检索       最终回答
             |             |
             +----->       v
                       来源引用
                           |
                           v
                         返回用户
```

## 9.3 Agent State

需要建立统一 Agent State。

建议字段：

```python
class AgentState(TypedDict):

    conversation_id: str

    user_id: str

    question: str

    conversation_history: list

    intent: str

    task_plan: list

    tool_calls: list

    tool_results: list

    retrieved_documents: list

    evidence: list

    answer: str

    citations: list

    iteration_count: int

    error: str | None

    status: str
```

以上为初始设计示意，实际实现需要根据 LangGraph 的状态更新和并行执行方式进一步定义类型。

State 需要支持：

- 多步骤执行。
- 工具执行结果保存。
- 失败状态记录。
- 中间结果传递。
- Checkpoint。
- 中断与恢复。
- 对话上下文管理。

## 9.4 Agent Tools 设计

所有业务能力通过工具暴露给 Agent。

第一期建议实现以下工具。

### Knowledge Tools

| Tool | 功能 |
|---|---|
| search_knowledge | 企业知识库检索 |
| search_fragment | 历史问答和专家经验检索 |
| get_document_content | 获取文档内容 |

### File Tools

| Tool | 功能 |
|---|---|
| search_file | 文件检索 |
| search_directory | 目录检索 |
| get_directory_children | 获取目录子节点 |
| get_directory_tree | 获取目录树 |
| get_file_detail | 获取文件元数据 |
| get_file_path | 获取完整路径 |
| get_file_content | 读取文件内容 |

### Database Tools

| Tool | 功能 |
|---|---|
| query_business_data | 结构化业务数据查询 |
| get_project_info | 项目基本信息查询 |

### Image Tools

| Tool | 功能 |
|---|---|
| analyze_image | 图片识别 |
| get_image_description | 获取图片描述 |

### CAD Tools

| Tool | 功能 |
|---|---|
| search_cad_drawing | 搜索 CAD 图纸 |
| get_cad_metadata | 获取图纸元数据 |
| get_cad_preview | 获取图纸预览 |

### Web Tools

| Tool | 功能 |
|---|---|
| web_search | 外部互联网搜索 |

### Preview Tools

| Tool | 功能 |
|---|---|
| get_document_preview | 获取文档预览 |
| get_file_download_url | 获取授权下载地址 |

所有 Tool 必须具有清晰的输入 Schema 和输出 Schema。

工具执行结果必须结构化，不应只返回不受约束的自然语言字符串。

## 9.5 典型 Agent 业务流程

用户：

“帮我查找公司以前做过的商业综合体项目，找出相关的建筑设计方案，分析这些项目的设计特点。”

执行过程：

1. Agent 识别为多步骤项目分析任务。
2. 调用 search_knowledge 或项目检索 Tool 查找商业综合体项目。
3. 调用 search_directory 定位项目目录。
4. 调用 get_directory_children 获取目录内容。
5. 调用 search_file 找到建筑设计方案。
6. 调用 get_file_content 获取相关文档内容。
7. 调用 RAG 对多个方案进行检索和上下文整理。
8. 将多个项目的证据传入分析节点。
9. LLM 进行对比分析。
10. 结果校验节点检查证据是否充分。
11. 返回综合分析结果及每个项目对应的文件引用。

---

# 第十章 结构化数据库查询 Agent

## 10.1 业务目标

支持用户通过自然语言查询企业其他业务系统中的结构化数据。

例如：

- 公司去年完成了多少个项目？
- 某个项目的建筑面积是多少？
- 某个项目当前进度如何？
- 某个部门今年承担了多少设计项目？

## 10.2 技术方案

采用 Text-to-SQL + 受控 SQL Tool。

执行流程：

```text
用户问题
   |
   v
SQL Agent
   |
   v
识别业务查询意图
   |
   v
获取允许访问的 Schema
   |
   v
生成 SQL
   |
   v
SQL Parser / Validator
   |
   v
权限检查
   |
   v
只读数据库执行
   |
   v
返回结构化结果
   |
   v
LLM 自然语言解释
```

## 10.3 安全要求

- 使用只读数据库账号。
- 禁止任意 DDL。
- 禁止任意 DML。
- 限制可访问表。
- 限制可访问字段。
- 限制查询条数。
- 限制执行时间。
- 校验用户数据权限。
- 禁止 SQL 绕过权限过滤。
- 记录 SQL 执行日志。

优先采用预定义业务查询接口或受控 Text-to-SQL。

不得让 Agent 获得企业生产数据库的管理员权限。

---

# 第十一章 Agent Harness 设计

本项目需要具备工程化 Agent Runtime，而不仅仅是使用 LangGraph 组织几个节点。

Harness 负责控制 Agent 的执行过程、上下文、工具和安全策略。

重点实现：

## 11.1 Context Engineering

负责：

- 对话历史管理。
- 历史消息裁剪。
- 上下文压缩。
- 检索结果筛选。
- Prompt 模板管理。
- Token 预算控制。
- 当前任务上下文隔离。

不能将全部历史对话和全部检索结果无限制地传给 LLM。

## 11.2 Tool Runtime

负责：

- Tool 注册。
- Tool Schema 管理。
- Tool 参数校验。
- Tool 权限检查。
- Tool 执行。
- Tool 超时控制。
- Tool 失败重试。
- Tool 调用日志。
- Tool 执行结果标准化。

## 11.3 Hooks

设计可插拔的执行生命周期钩子。

建议支持：

| Hook | 触发时机 | 用途 |
|---|---|---|
| BeforeAgent | Agent 开始前 | 用户权限和上下文初始化 |
| BeforeModel | 模型调用前 | Prompt 检查、数据分级 |
| AfterModel | 模型调用后 | 输出检查 |
| BeforeTool | 工具调用前 | 参数及权限校验 |
| AfterTool | 工具调用后 | 结果审计 |
| OnError | 发生异常时 | 错误处理 |
| AfterAgent | Agent 结束后 | 轨迹保存、Token 统计 |

Hooks 需要采用统一注册机制，避免将全部逻辑硬编码在 Agent 节点中。

## 11.4 Checkpoint

基于 LangGraph Checkpointer 实现状态持久化。

支持：

- 执行状态保存。
- 多轮对话。
- 中断恢复。
- 长任务恢复。
- Human-in-the-loop（必要时）。
- 执行轨迹追踪。

## 11.5 Agent 执行安全

- 最大执行步骤限制。
- 最大 Tool 调用次数限制。
- 最大循环次数限制。
- 单次模型调用超时。
- 工具执行超时。
- 异常重试上限。
- 敏感操作人工确认。
- Tool 权限校验。
- Prompt Injection 防护。

---

# 第十二章 企业级安全体系

安全是整个系统的基础能力。

## 12.1 用户权限

采用企业统一身份认证。

Java Spring Security 负责用户认证及授权。

Agent 请求必须携带可信用户身份信息。

不能依赖 LLM 自己判断用户是否有权限。

## 12.2 数据权限

文件、目录、文档 Chunk、图纸、数据库记录均需要关联权限范围。

权限检查需要在检索之前完成。

不能只在最终答案阶段检查权限。

## 12.3 云端模型安全

建立云端模型调用策略：

- L3 数据禁止上传。
- L2 数据默认本地处理。
- L1 数据允许按策略调用云端模型。
- 必要时进行脱敏。
- 记录云端调用审计日志。

## 12.4 Prompt Injection

需要防止文档中的恶意指令影响 Agent 行为。

原则：

- 知识库内容只作为参考数据，不作为系统指令。
- Tool 参数必须经过校验。
- 不允许检索内容修改系统权限。
- 不允许文档要求 Agent 调用未经授权的工具。
- 所有外部搜索结果作为不可信数据处理。

---

# 第十三章 API 设计

Java Spring Boot 对外提供业务接口，Python FastAPI 提供 Agent 内部接口。

## 13.1 Agent API

### 创建对话

`POST /api/agent/chat`

请求：

```json
{
  "conversation_id": null,
  "question": "帮我找一下公司以前做过的商业综合体项目",
  "stream": true
}
```

### 获取执行状态

`GET /api/agent/tasks/{task_id}`

### 获取对话历史

`GET /api/agent/conversations/{conversation_id}`

### 获取执行轨迹

`GET /api/agent/tasks/{task_id}/trace`

## 13.2 文件管理 API

| 接口 | 功能 |
|---|---|
| POST /api/files/upload | 上传文件 |
| GET /api/files/{id} | 文件详情 |
| GET /api/files/{id}/path | 完整路径 |
| GET /api/files/{id}/preview | 文件预览 |
| GET /api/directories/{id}/children | 目录子节点 |
| GET /api/files/search | 文件检索 |

## 13.3 知识库管理 API

| 接口 | 功能 |
|---|---|
| POST /api/knowledge/import | 导入知识 |
| GET /api/knowledge/tasks | 查询解析任务 |
| GET /api/knowledge/files/{id} | 文件解析详情 |
| POST /api/knowledge/reindex | 重新索引 |
| DELETE /api/knowledge/files/{id} | 删除知识文件 |

## 13.4 API 设计要求

- 统一返回结构。
- 统一异常处理。
- 统一身份认证。
- 参数校验。
- 分页查询。
- 操作日志。
- 权限检查。
- SSE 流式回答。
- 文件下载权限控制。

---

# 第十四章 项目代码结构

建议采用 Monorepo，Java 和 Python 分开管理。

```text
building-agent/
│
├── frontend/
│   └── Vue 前端项目
│
├── backend/
│   └── Java Spring Boot
│       ├── auth/
│       ├── user/
│       ├── permission/
│       ├── file/
│       ├── directory/
│       ├── knowledge/
│       ├── conversation/
│       ├── agent/
│       └── common/
│
├── agent-service/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── agent/
│   │   │   ├── graph.py
│   │   │   ├── state.py
│   │   │   ├── nodes/
│   │   │   ├── routers/
│   │   │   ├── prompts/
│   │   │   └── checkpoints/
│   │   │
│   │   ├── tools/
│   │   │   ├── knowledge/
│   │   │   ├── file/
│   │   │   ├── database/
│   │   │   ├── image/
│   │   │   ├── cad/
│   │   │   └── web/
│   │   │
│   │   ├── rag/
│   │   │   ├── embedding/
│   │   │   ├── retriever/
│   │   │   ├── hybrid_search/
│   │   │   ├── reranker/
│   │   │   └── context/
│   │   │
│   │   ├── model_gateway/
│   │   │   ├── llm.py
│   │   │   ├── vision.py
│   │   │   ├── embedding.py
│   │   │   └── router.py
│   │   │
│   │   ├── harness/
│   │   │   ├── hooks/
│   │   │   ├── context/
│   │   │   ├── middleware/
│   │   │   ├── execution/
│   │   │   └── security/
│   │   │
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config/
│   │   └── utils/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── ingestion-service/
│   ├── parsers/
│   │   ├── word_parser.py
│   │   ├── pdf_parser.py
│   │   ├── ppt_parser.py
│   │   ├── excel_parser.py
│   │   ├── image_parser.py
│   │   ├── cad_parser.py
│   │   └── fragment_parser.py
│   │
│   ├── pipeline/
│   ├── chunking/
│   ├── embedding/
│   ├── workers/
│   └── tests/
│
├── infrastructure/
│   ├── docker-compose.yml
│   ├── postgres/
│   ├── elasticsearch/
│   ├── minio/
│   ├── redis/
│   ├── rabbitmq/
│   ├── vllm/
│   └── monitoring/
│
├── docs/
│   ├── architecture.md
│   ├── database-design.md
│   ├── api-design.md
│   └── deployment.md
│
└── README.md
```

目录结构允许在实际开发中调整，但应保持 Agent、知识处理、模型网关和业务服务之间的职责边界。

---

# 第十五章 开发实施计划

建议分阶段交付，不要一次性生成整个项目的全部功能。

## 第一阶段：基础工程与 Agent 核心引擎

目标：

建立最小可运行的 Agent。

实现：

1. Spring Boot 基础服务。
2. FastAPI Agent 服务。
3. LangGraph 基础工作流。
4. Model Gateway。
5. 本地模型调用。
6. 云端模型调用。
7. Agent State。
8. Tool Calling。
9. 基础对话接口。
10. SSE 流式回答。

验收标准：

用户能够输入问题，Agent 能够调用模型并完成一次基础回答。

## 第二阶段：知识库基础设施

实现：

1. PostgreSQL。
2. pgvector。
3. Elasticsearch。
4. MinIO。
5. Redis。
6. RabbitMQ。
7. 文件上传。
8. 文件元数据管理。
9. 多层级目录管理。
10. 文件去重和增量更新。

验收标准：

能够上传文件，保存文件信息，维护完整目录树。

## 第三阶段：多模态数据解析

实现：

1. Word Parser。
2. PDF Parser。
3. PPT Parser。
4. Excel Parser。
5. 图片 OCR。
6. VLM 图片描述。
7. 知识碎片 Parser。
8. CAD Parser。
9. Chunk。
10. Embedding。
11. 异步任务处理。

验收标准：

支持上述文件的解析和知识索引构建，并能够追踪处理状态。

## 第四阶段：企业级 RAG

实现：

1. Embedding 检索。
2. BM25 检索。
3. Hybrid Search。
4. RRF。
5. Reranker。
6. Metadata Filtering。
7. Context Assembly。
8. 文档来源引用。

验收标准：

用户可以通过自然语言查询知识库，并获得带真实来源的回答。

## 第五阶段：Agent Tools

实现：

1. Knowledge Tools。
2. File Tools。
3. Directory Tools。
4. SQL Tools。
5. Image Tools。
6. CAD Tools。
7. Web Search Tools。
8. Preview Tools。

验收标准：

Agent 能够根据用户问题选择正确工具，并能够组合多个工具完成任务。

## 第六阶段：Agent Harness

实现：

1. Context Engineering。
2. Hooks。
3. Checkpoint。
4. Tool Runtime。
5. 错误恢复。
6. 执行次数限制。
7. 权限控制。
8. 执行轨迹追踪。

验收标准：

Agent 能够执行多步骤任务，支持状态保存、失败恢复和安全控制。

## 第七阶段：安全、部署及性能优化

实现：

1. 用户权限体系。
2. 数据权限过滤。
3. 云端模型数据安全。
4. Docker 部署。
5. Prometheus。
6. Grafana。
7. Langfuse。
8. 性能测试。
9. 检索评估。
10. 生产部署文档。

验收标准：

系统可以在企业内网部署运行，具备基本的监控、安全和性能评估能力。

---

# 第十六章 测试与质量评估

## 16.1 Agent 测试

测试以下场景：

- 普通问题回答。
- 多步骤任务规划。
- 多 Tool 组合调用。
- Tool 执行失败。
- 模型调用失败。
- 任务中断恢复。
- 超出最大执行次数。
- 权限不足。

## 16.2 RAG 测试

建议构建专业测试集。

评估指标：

| 指标 | 说明 |
|---|---|
| Recall@K | 正确知识是否进入召回结果 |
| Precision@K | 召回结果的准确程度 |
| MRR | 正确结果的排名表现 |
| NDCG@K | 排序质量 |
| Faithfulness | 回答是否忠于检索证据 |
| Answer Relevance | 回答与问题的相关程度 |
| Citation Accuracy | 来源引用准确程度 |

## 16.3 文档解析测试

评估：

- 文件解析成功率。
- OCR 准确率。
- 表格提取准确率。
- 标题层级保留情况。
- 页码关联准确率。
- 文件增量更新正确率。

## 16.4 系统性能测试

评估：

- 文件处理吞吐量。
- Embedding 吞吐量。
- 检索 P95 延迟。
- Agent 平均响应时间。
- Agent 多步骤任务成功率。
- 并发用户数量。
- 模型 Token 消耗。
- GPU 显存占用。

具体性能指标需要根据硬件和真实数据压测后确定，不预先虚构性能承诺。

---

# 第十七章 第一版 MVP 范围

为了避免开发范围过大，第一期不应该一次性完成所有复杂功能。

建议 MVP 优先实现：

1. 用户能够与 Agent 对话。
2. Agent 支持本地 LLM 和云端 API。
3. 支持 Word、PDF、PPT、Excel 导入。
4. 支持多层级目录树。
5. 支持文件名称及路径检索。
6. 支持文档内容 RAG。
7. 支持 BM25 + 向量混合检索。
8. 支持 Reranker。
9. 支持文件来源引用。
10. 支持基础 Tool Calling。
11. 支持 Agent 多步骤执行。
12. 支持基本用户权限。

第二期再增加：

- 图片 VLM。
- Web Search。
- CAD 图纸解析。
- 结构化数据库 Text-to-SQL。
- 专家论坛和历史问答。
- 完整 Agent Harness。
- 高级权限和可观测性。

---

# 第十八章 交给 Coding Agent 的开发指令

请严格遵循以下开发要求。

## 18.1 开发原则

1. 不要一次性生成整个项目。
2. 严格按照开发阶段逐步实施。
3. 每个阶段必须能够独立运行。
4. 每个模块必须有清晰的职责边界。
5. 优先使用成熟、稳定的开源技术。
6. 不要为了使用新技术而引入不必要的复杂度。
7. 所有模型调用通过统一 Model Gateway。
8. 所有 Agent 工具必须定义清晰的输入和输出 Schema。
9. 所有文件和知识片段必须保留来源信息。
10. 所有检索操作必须经过权限检查。
11. 不允许模型自行编造文件路径和文件来源。
12. 不允许 Agent 直接访问生产数据库。
13. 不允许将敏感企业数据未经授权发送到云端。
14. 所有关键功能必须编写单元测试和集成测试。
15. 所有配置通过环境变量或配置文件管理，不允许将密钥硬编码到代码中。

## 18.2 开发协作要求

每个开发阶段开始前：

1. 阅读本技术设计文档。
2. 检查现有代码。
3. 明确本阶段目标。
4. 给出具体实现方案。
5. 明确需要新增和修改的文件。
6. 明确依赖组件。
7. 明确数据库变更。
8. 明确验收标准。

完成后：

1. 运行代码检查。
2. 运行单元测试。
3. 运行必要的集成测试。
4. 检查异常处理。
5. 检查配置完整性。
6. 更新 README。
7. 更新技术文档。
8. 汇报已实现功能、未完成内容和已知问题。

不得只生成代码而不验证代码是否可运行。

## 18.3 当前第一项开发任务

现在不要直接实现全部业务功能。

首先完成第一阶段：基础工程与 Agent 核心引擎。

具体任务：

1. 创建 Monorepo 项目结构。
2. 创建 Spring Boot 项目。
3. 创建 FastAPI 项目。
4. 集成 LangGraph。
5. 实现统一 Model Gateway。
6. 实现本地模型和云端模型配置接口。
7. 实现基础 Agent State。
8. 实现一个最简单的 LangGraph 工作流。
9. 实现一个示例 Tool，例如 get_current_time 或 search_demo。
10. 实现 Agent Tool Calling。
11. 实现 Spring Boot 调用 FastAPI。
12. 实现 SSE 流式回答。
13. 编写 Docker Compose 基础配置。
14. 编写启动说明和测试用例。

第一阶段暂时不接入真实企业数据，不实现完整 RAG，不实现复杂多模态解析。

先保证最小 Agent 闭环真正运行：

```text
用户提问
   |
   v
Spring Boot
   |
   v
FastAPI
   |
   v
LangGraph
   |
   v
LLM 判断是否需要调用 Tool
   |
   v
Tool 执行
   |
   v
LLM 根据 Tool 结果生成回答
   |
   v
SSE 返回用户
```

完成后再进入第二阶段。

---

# 第十九章 项目最终目标

最终建成一个具备以下能力的企业级 Agent 系统：

- 支持多源异构企业知识接入。
- 支持多模态文档解析。
- 支持企业级 Hybrid RAG。
- 支持多层级目录精准定位。
- 支持图片识别与外部信息搜索。
- 支持 CAD 图纸索引、OCR 和展示。
- 支持企业结构化数据库查询。
- 支持 Agent 多步骤任务规划与执行。
- 支持本地和云端模型动态路由。
- 支持 Agent Harness 工程化控制。
- 支持企业用户和数据权限隔离。
- 支持来源追溯、执行审计和系统监控。
- 支持私有化部署。

项目的核心定位不是简单的 RAG 问答系统，而是：

**以 Agent 为任务执行核心，以 RAG 为企业知识获取能力，以多模态解析为数据基础，以 Model Gateway 为模型调度中心，以 Agent Harness 为运行控制体系的企业级多模态智能知识系统。**

文档结束。