from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI
import os  # 建议增加 os 库来读取环境变量

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def instant():
    # 修改点：传入 base_url 指向中转服务器
    client = OpenAI(
        api_key=os.environ.get(process.env.OPENAI_API_KEY), # 从环境变量读取
        base_url="https://api.siliconflow.cn/v1"  # 替换为你中转站的地址
    )
    
    message = """
    You are on a website that has just been deployed to production for the first time!
    Please reply with an enthusiastic announcement...
    """
    
    messages = [{"role": "user", "content": message}]
    
    # 修改点：模型名称要对应中转站支持的模型，例如 "vendor/gpt-4o" 或 "deepseek-v3"
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3.2", # 确保中转站有这个模型，截图里的 gpt-5-nano 目前是占位符
        messages=messages
    )
    
    reply = response.choices[0].message.content.replace("\n", "<br/>")
    html = f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"
    return html
    