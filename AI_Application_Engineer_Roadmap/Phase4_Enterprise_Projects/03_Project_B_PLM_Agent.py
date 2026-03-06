import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

# ==========================================
# 杀手锏项目 B: 模拟研发流程自动化 Agent 平台
# ==========================================
# 背景：这个脚本模拟了一个车企的 PLM 和仿真系统的内部微服务。
# 你的任务（作为 Agent 开发者）：
# 使用 LangChain / AutoGen 编写一个 Agent，赋予它调用这个 FastAPI 接口的权限（作为工具 Tools）。
# 让用户可以通过自然语言说：“帮我查一下底盘转向节(Knuckle)最新的仿真测试结果，如果应力超过 300MPa，就帮我发一封警告邮件。”
# Agent 会自主思考并调用本脚本模拟的接口。

app = FastAPI(title="Mock Automotive R&D Systems API")

# 模拟的后端数据库
MOCK_PLM_DB = {
    "P1001": {"name": "转向节(Knuckle)", "material": "铝合金", "status": "设计中", "owner": "Li Lei"},
    "P1002": {"name": "避震弹簧", "material": "高碳钢", "status": "已量产", "owner": "Han Meimei"}
}

MOCK_CAE_SIMULATION_DB = {
    "P1001": {"test_id": "SIM-998", "max_stress_mpa": 315.5, "result": "Failed"},
    "P1002": {"test_id": "SIM-902", "max_stress_mpa": 180.2, "result": "Passed"}
}

# -----------------
# 模拟系统接口 (Tools 候选)
# -----------------

@app.get("/api/plm/part/{part_id}")
async def query_part_info(part_id: str):
    """【Tool 1】查询 PLM 系统中的零部件基本信息"""
    if part_id in MOCK_PLM_DB:
        return {"status": "success", "data": MOCK_PLM_DB[part_id]}
    return {"status": "error", "message": "Part not found"}

@app.get("/api/cae/result/{part_id}")
async def query_simulation_result(part_id: str):
    """【Tool 2】查询 CAE 仿真平台中的零件强度测试结果"""
    if part_id in MOCK_CAE_SIMULATION_DB:
        return {"status": "success", "data": MOCK_CAE_SIMULATION_DB[part_id]}
    return {"status": "error", "message": "No simulation record found for this part"}

class EmailRequest(BaseModel):
    to_user: str
    subject: str
    body: str

@app.post("/api/email/send")
async def send_warning_email(request: EmailRequest):
    """【Tool 3】调用公司内部邮件系统发送警告"""
    print(f"\n[模拟邮件发送成功] -> To: {request.to_user}")
    print(f"Subject: {request.subject}")
    print(f"Body: {request.body}\n")
    return {"status": "success", "message": "Email sent"}

# -----------------
# 面试指导思路
# -----------------
"""
在面试中介绍这个项目时，你可以这么说：
'为了解决研发工程师跨多个系统（PLM看BOM，CAE看仿真结果）导致效率低下的问题，
我设计并实现了一个基于 LLM Tool Calling 的研发助理 Agent。
我将各个业务系统的 OpenAPI 封装成了 LangChain 的 Tools。
当工程师提问时，Agent 会利用 ReAct 范式，先调用 PLM 接口将模糊的零件名转换为准确的零件号，
然后自动将零件号传入 CAE 接口获取应力数据。
如果发现数据异常，Agent 会自动拼接报告，调用内部消息总线发送飞书/邮件提醒。
这极大地减少了工程师在不同工业软件间切回操作的时间。'
"""

if __name__ == "__main__":
    import uvicorn
    # 启动命令: python 03_Project_B_PLM_Agent.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
