# test_chat_api.py
import pytest
import requests
from sseclient import SSEClient  # 需要安装sseclient-py

# 服务器配置
SERVER_HOST = "http://localhost"
SERVER_PORT = 8000
BASE_URL = f"{SERVER_HOST}:{SERVER_PORT}"

request_data = {
    "query": "你好",
    "conversation_id": "test_id",
    "model_name": "deepseek-chat",
    "prompt_name": "general_chat"
}


def test_sse_streaming_success():
    """测试正常流式输出"""

    response = requests.post(
        f"{BASE_URL}/api/chat",
        json=request_data,
        headers={"Accept": "text/event-stream"},
        stream=True
    )

    # 验证响应头
    assert response.status_code == 200
    assert "text/event-stream" in response.headers['Content-Type']

    # 使用SSEClient解析事件流
    client = SSEClient(response)
    received_events = []

    # 收集事件（设置超时防止无限等待）
    try:
        for event in client.events():
            received_events.append(event)
            if len(received_events) >= 3:  # 根据实际情况调整
                break
    except requests.exceptions.ChunkedEncodingError:
        pass

    # 基础验证
    assert len(received_events) > 0
    for event in received_events:
        assert event.data  # 验证每个事件都有数据
        print(event.data)
        # 如果需要验证JSON格式
        # json_data = json.loads(event.data)
        # assert "text" in json_data


if __name__ == "__main__":
    pytest.main(["-v", __file__, "playground/test_chat_api.py::test_sse_streaming_success"])
