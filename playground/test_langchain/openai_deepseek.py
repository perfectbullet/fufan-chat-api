# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

# client = OpenAI(api_key="sk-aae01ef2678e4200a51c8a3f8b9c9313", base_url="https://api.deepseek.com")

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "hai"},
#     ],
#     stream=False
# )
#
# print(response.choices[0].message.content)



# ############################ deepseek 参考
# https://python.langchain.com/docs/integrations/chat/deepseek/
import getpass
import os

if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = "sk-aae01ef2678e4200a51c8a3f8b9c9313"

from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
# # Invocation
# messages = [
#     (
#         "system",
#         "你是一个帮助将英文翻译成中文的助手。请翻译用户提供的句子。",
#     ),
#     ("human", "You are a helpful assistant that translates English to Chinese. Translate the user sentence."),
# ]
# ai_msg = llm.invoke(messages)
#
# print('ai_msg.content: ', ai_msg.content)

# ########### chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "你是一个帮助将{input_language}翻译成{output_language}的助手。请翻译用户提供的句子。",
        ),
        ("human", "{input}"),
    ]
)


chain = prompt_template | llm
res = chain.invoke({
        "input_language": "英文",
        "output_language": "中文",
        "input": "I love programming.",
    })
print(res)
