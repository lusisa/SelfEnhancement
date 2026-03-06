# Phase 3: RAG 检索增强生成架构解析

RAG (Retrieval-Augmented Generation) 是目前企业级 AI 落地最成熟的方案。它解决了大模型缺乏私有知识和产生幻觉的问题。

## RAG 核心链路 (四大核心组件)

### 1. Indexing (数据索引阶段，通常离线运行)
将企业的 PDF、Word、数据库记录变成大模型可以理解的向量。

*   **Document Loading (文档加载)**: 使用工具 (如 LangChain 的 DocumentLoaders) 读取文件。
*   **Text Splitting/Chunking (文本切分)**: 把几百页的 PDF 切成一小块一小块 (Chunks)。
    *   **核心痛点**: 切小了丢失上下文，切大了超出 Context Window。通常需要配合 Overlap (重叠) 来保证语义连贯。
*   **Embedding (向量化)**: 将 Chunk 喂给 Embedding 模型 (如 text-embedding-3-small, BGE)，将文本变成高维浮点数数组。语义相近的句子，其向量在空间中的距离也相近。
*   **Vector Database (向量数据库)**: 存储这些 Chunk 和它们对应的向量。常用的有 Chroma, Milvus, Qdrant, Pinecone。

### 2. Retrieval (检索阶段，在线运行)
当用户提问时，如何在海量库中找到相关内容。

*   将用户的 Query 同样用 Embedding 模型转成向量。
*   在向量数据库中进行相似度搜索 (如 Cosine Similarity 余弦相似度)，找出 Top-K 个最相关的 Chunk。

### 3. Generation (生成阶段)
将检索出来的 Top-K 个 Chunk 作为 Context (上下文)，配合用户的 Query 一起塞进 Prompt 中，发给大模型。

*   *Prompt 示例*: "请根据以下提供的信息回答用户问题。如果信息中没有答案，请说不知道。信息：{context}，问题：{query}"

### 4. Advanced RAG (高阶优化，高级工程师必考)
基础 RAG 往往效果不佳，需要高阶手段优化：
*   **Query Transformation (查询重写)**: 用户的提问往往简短且模糊，先用一个小 LLM 把用户的 Query 扩写或拆解成多个子 Query，再分别去检索。
*   **Hybrid Search (混合检索)**: 向量检索 (找语义相似) + 关键词检索 (找完全匹配的专有名词如零件号BM-1002)。两者结合 (如通过 BM25 算法)。
*   **Reranking (重排)**: 检索出来的几十个结果可能不太准，使用专门的 Rerank 模型 (如 BAAI/bge-reranker) 对这几十个结果重新打分排序，只把最精华的 5 个喂给最终的生成模型。