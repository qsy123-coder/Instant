from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

# 确保在初始化 app 之前加载环境
load_dotenv(".env.local", override=True)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def instant():
    # 1. 必须先获取变量名，才能在后面做判断
    current_api_key = os.environ.get("OPENAI_API_KEY")
    current_base_url = os.environ.get("OPENAI_API_BASE_URL")

    # 2. 增加防御性判断
    if not current_api_key:
        return "<html><body><h1>Configuration Error</h1><p>API Key is missing. 请运行 vercel env pull 并检查 .env.local 文件</p></body></html>"

    try:
        # 3. 使用获取到的变量初始化
        client = OpenAI(
            api_key=current_api_key,
            base_url=current_base_url
        )
        
        message = "Are you okay? Please reply in a friendly way."
        
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3", 
            messages=[{"role": "user", "content": message}],
            timeout=15.0
        )
        
        reply = response.choices[0].message.content.replace("\n", "<br/>")
        return f"<html><body><p>{reply}</p></body></html>"
        
    except Exception as e:
        # 如果还是报错，这里会告诉你具体是 Key 错了还是网络不通
        return f"<html><body><h1>Runtime Error</h1><p>{str(e)}</p></body></html>"