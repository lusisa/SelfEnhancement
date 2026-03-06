import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 这是一个使用 LangChain 构建基础调用链 (Chain) 的演示。
# LangChain 是将 LLM 的输入输出与业务逻辑解耦的优秀框架 (使用 LCEL 表达式)。

# 1. 实例化 LLM 模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    # api_key="your_api_key_here" # 建议配置在环境变量 OPENAI_API_KEY 中
)

# 2. 构造 Prompt 模板
# 通过占位符 {topic} 动态注入变量
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深的汽车行业分析师，专门解答关于 {topic} 的问题。"),
    ("user", "{question}")
])

# 3. 构造 Output Parser
# 它的作用是将 LLM 返回的复杂消息对象，提取为纯文本字符串
output_parser = StrOutputParser()

# 4. 构建 LCEL (LangChain Expression Language) 处理链
# 管道符 `|` 的意义： prompt 渲染后的结果传给 llm，llm 的结果传给 output_parser
chain = prompt | llm | output_parser

def run_chain_demo():
    print("=== LangChain 基础 Chain 运行演示 ===\n")
    
    # 我们要问关于 "新能源汽车电池技术" 的问题
    topic = "新能源汽车电池技术"
    question = "目前固态电池相比于传统的液态锂电池，最大的三个优势是什么？请简练回答。"
    
    print(f"正在向 AI 提问...\n主题: {topic}\n问题: {question}\n")
    
    try:
        # invoke 触发整条链路
        result = chain.invoke({
            "topic": topic,
            "question": question
        })
        print(f"AI 分析结果:\n{result}")
        
    except Exception as e:
        print(f"调用出错: 请检查你的 API_KEY 或网络连通性。\n错误详情: {e}")

if __name__ == "__main__":
    run_chain_demo()
