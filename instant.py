from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

# 自动寻找 .env 文件（本地）或读取系统变量（Vercel）
load_dotenv() 

app = FastAPI()

# 建议将 Client 放在函数外部，这样可以复用连接，提高性能
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url="https://api.siliconflow.cn/v1"
)

@app.get("/", response_class=HTMLResponse)
def instant():
    # 检查 Key 是否读取成功的简单调试逻辑
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: API Key not found in environment variables."

    message = "You are on a website that has just been deployed... reply with enthusiasm!"
    
    # 注意：DeepSeek 的模型名称通常为 deepseek-ai/DeepSeek-V3 
    # 请确认 SiliconFlow 平台上该模型的准确 ID
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3", 
        messages=[{"role": "user", "content": message}]
    )
    
    reply = response.choices[0].message.content.replace("\n", "<br/>")
    return f"<html><body><p>{reply}</p></body></html>"