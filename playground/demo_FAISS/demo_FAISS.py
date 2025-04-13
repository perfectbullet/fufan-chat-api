import os

from langchain_community.vectorstores import FAISS

if not os.getenv("ZHIPUAI_API_KEY"):
    os.environ["ZHIPUAI_API_KEY"] = '53c8378d900c4f31bdbe6d564b33c0f8.Ta4Z1YRszdFJfhL3'


# 1. 加载文本文件
from text_splitter.chinese_recursive_text_splitter import ChineseRecursiveTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader("README.md", encoding="utf-8")
documents = loader.load()

# 2. 文本切分
text_splitter = ChineseRecursiveTextSplitter(
    keep_separator=True,
    is_separator_regex=True,
    chunk_size=100,
    chunk_overlap=20
)
docs = text_splitter.split_documents(documents)

# 3. 文本向量化
from langchain_community.embeddings import ZhipuAIEmbeddings

embeddings = ZhipuAIEmbeddings(
    model="embedding-3",
    # With the `embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)

# 4. 构建FAISS索引
vectorstore = FAISS.from_documents(docs, embeddings)

# 5. 保存索引（可选）
faiss_index_name = 'faiss_index'
vectorstore.save_local(faiss_index_name)


# 6. 保存索引（可选）
# 加载已经保存的索引
vectorstore = FAISS.load_local(faiss_index_name, embeddings, allow_dangerous_deserialization=True)

# 7. 执行向量相似度查询
query = "大模型应用技术原理"
docs_and_scores = vectorstore.similarity_search_with_score(query, k=3)

# 输出结果
for doc, score in docs_and_scores:
    print(f"Score: {score:.4f}")
    print(doc.page_content)
    print("-" * 50)

# 8. 删除
import shutil
shutil.rmtree(faiss_index_name)