import requests
import json

# OpenAI-compatible vLLM embedding endpoint
API_URL = "http://localhost:8000/v1/embeddings"

# 模型名称（与 docker-compose.yml 中的 --served-model-name 一致）
MODEL_NAME = "bge-embedding"

# 要生成 embedding 的文本列表
input_texts = [
    "vLLM is incredibly fast.",
    "Embeddings help measure semantic similarity."
]

# 构造请求数据
payload = {
    "model": MODEL_NAME,
    "input": input_texts
}

headers = {
    "Content-Type": "application/json"
}

if __name__ == '__main__':

    # 发送 POST 请求
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    # 解析并输出结果
    if response.status_code == 200:
        data = response.json()
        for i, item in enumerate(data["data"]):
            print(f"\nInput {i+1}: {input_texts[i]}")
            print(f"Embedding (前10维): {item['embedding'][:10]} ...")
    else:
        print("请求失败:", response.status_code)
        print(response.text)
