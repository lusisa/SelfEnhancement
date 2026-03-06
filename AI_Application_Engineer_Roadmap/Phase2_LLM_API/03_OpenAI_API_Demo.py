import os
import asyncio
from openai import AsyncOpenAI
# 注意：你需要安装 openai 库：pip install openai python-dotenv
# 这里以使用 OpenAI 官方接口为例，你可以通过修改 base_url 和 api_key 轻松切换至智谱、通义千问等国内大模型。

# 初始化异步的 OpenAI 客户端
# 请确保你的环境变量中设置了 OPENAI_API_KEY
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"),
    # 如果使用国内的中转代理或其他模型，可以在这里修改：
    # base_url="https://api.deepseek.com/v1" 
)

async def simple_chat(prompt: str):
    print(f"\n[用户]: {prompt}")
    print("[AI思考中...]")
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo", # 根据你的实际 key 支持的模型修改
            messages=[
                {"role": "system", "content": "你是一位专业的车企研发工程师助手，请用简洁专业的话语回答问题。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        print(f"[AI回复]: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"调用 API 失败: {e}")

async def streaming_chat(prompt: str):
    print(f"\n[用户]: {prompt} (流式输出模式)")
    print("[AI回复]: ", end="", flush=True)
    
    try:
        # stream=True 是实现打字机效果的关键
        stream_response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=True,
            temperature=0.7
        )
        
        async for chunk in stream_response:
            # 增量打印内容
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print() # 换行
        
    except Exception as e:
        print(f"\n流式调用 API 失败: {e}")

async def main():
    # 演示普通调用
    await simple_chat("在汽车研发中，什么是BOM(物料清单)？简单解释下。")
    
    # 演示流式输出调用
    await streaming_chat("写一个简短的关于自动驾驶的科幻故事开头。")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
