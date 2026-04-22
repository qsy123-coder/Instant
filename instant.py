from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def instant():
    # 1. 运行时获取 Key
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # 2. 增加防御性判断，防止直接 Crash
    if not api_key:
        return "<html><body><h1>Configuration Error</h1><p>API Key is missing in Vercel settings.</p></body></html>"

    try:
        # 在函数内部初始化
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.siliconflow.cn/v1"
        )
        
        message = "You are on a website that has just been deployed! Reply with enthusiasm."
        
        # 3. 检查模型名称：SiliconFlow 常见的 ID 是 deepseek-ai/DeepSeek-V3
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3", 
            messages=[{"role": "user", "content": message}],
            timeout=15.0 # 建议加上超时，防止 Vercel 函数运行超时（默认 10s）
        )
        
        reply = response.choices[0].message.content.replace("\n", "<br/>")
        return f"<html><body><p>{reply}</p></body></html>"
        
    except Exception as e:
        # 将错误捕获并返回，而不是让函数 Crash
        return f"<html><body><h1>Runtime Error</h1><p>{str(e)}</p></body></html>"