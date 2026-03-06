from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio

# 这是一个演示如何使用 FastAPI 构建高并发后端的基础模板
# FastAPI 是目前 AI 应用最常使用的后端框架之一

app = FastAPI(title="Phase 1: FastAPI Basic Demo", description="车企AI应用工程师后端基础练习")

# 数据模型定义 (利用 Pydantic 进行类型校验)
class UserRequest(BaseModel):
    user_id: int
    query: str

class UserResponse(BaseModel):
    status: str
    message: str
    reply: str

# 模拟一个耗时的 AI 处理任务 (如调用大模型API)
async def mock_ai_process(query: str) -> str:
    print(f"正在处理查询: {query}...")
    await asyncio.sleep(2) # 模拟网络延迟
    return f"AI回复：我已经收到了你的问题 '{query}'"

# 1. 基础 GET 请求
@app.get("/")
async def root():
    return {"message": "Welcome to AI App Backend!"}

# 2. 带有路径参数的 GET 请求
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User_{user_id}"}

# 3. 带有请求体的 POST 请求 (核心重点)
@app.post("/chat", response_model=UserResponse)
async def chat_endpoint(request: UserRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="查询不能为空")
    
    # 使用 await 调用异步的 AI 处理函数
    reply = await mock_ai_process(request.query)
    
    return UserResponse(
        status="success",
        message="处理成功",
        reply=reply
    )

if __name__ == "__main__":
    # 使用 uvicorn 启动服务
    # 可以在终端运行: uvicorn 03_FastAPI_Basic:app --reload
    print("API 文档已就绪: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
