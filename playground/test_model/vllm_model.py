from openai import OpenAI
import os

# 设置临时环境变量
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['all_proxy'] = ''

base_url = "http://localhost:8000/v1/"
client = OpenAI(api_key="EMPTY", base_url=base_url)

pr = '''写一个关于AI的诗词'''
messages = [{"role": "user", "content": pr}]

response = client.chat.completions.create(
    model="DeepSeek-R1-Distill-Llama-8B",
    messages=messages,
)

print(response.choices[0].message.content)
