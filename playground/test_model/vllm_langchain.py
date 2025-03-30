import os

from langchain_openai import ChatOpenAI

# 设置临时环境变量
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['all_proxy'] = ''

# 初始化模型（需替换实际 API Key）base_url = "http://localhost:8000/v1/"
# client = OpenAI(api_key="EMPTY", base_url=base_url)
#
# pr = '''写一个关于AI的诗词'''
# messages = [{"role": "user", "content": pr}]
#
# response = client.chat.completions.create(
#     model="DeepSeek-R1-Distill-Llama-8B",
#     messages=messages,
# )
llm = ChatOpenAI(
    model="DeepSeek-R1-Distill-Llama-8B",
    openai_api_key="sk-xxx",
    base_url="http://localhost:8000/v1"  # 可替换为代理地址
)

# 单次调用
# response = llm.invoke("Java中的HashMap如何解决哈希冲突？")
# print(response.content)  # 输出模型响应内容[1,2](@ref)
# print('*' * 20)
# 批量调用
# batch_responses = llm.batch([
#     "写一首关于春天的诗",
#     "将'Hello World'翻译成法语"
# ])
# print(batch_responses)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 创建提示模板+模型+解析器的组合链
prompt = ChatPromptTemplate.from_template("用{style}风格解释：{topic}")
chain = prompt | llm | StrOutputParser()

# 流式调用
for chunk in chain.stream({"style": "幽默", "topic": "区块链技术"}):
    print(chunk, end="", flush=True)  # 输出示例：区块|链|就像|数字|乐高...[4](@ref)