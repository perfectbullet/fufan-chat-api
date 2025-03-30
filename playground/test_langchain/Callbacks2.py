import os

from langchain_core.callbacks.manager import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_deepseek import ChatDeepSeek

if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = "sk-aae01ef2678e4200a51c8a3f8b9c9313"

streaming_chat = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

messages = [
    AIMessage(content="你好"),
    SystemMessage(content="你是一位诗人"),
    HumanMessage(content="请你根据我的输入,帮我写一首关于小鸭子落水的诗"),
]

res = streaming_chat.invoke(messages)
print(res)
