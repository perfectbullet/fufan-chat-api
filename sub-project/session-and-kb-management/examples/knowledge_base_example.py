"""
知识库访问使用示例

本示例展示如何使用知识库访问模块进行知识库的创建、文档上传、向量检索和问答等操作。
"""

import asyncio
import uuid
from datetime import datetime


async def knowledge_base_example():
    """知识库访问完整示例"""
    
    print("=" * 60)
    print("知识库访问使用示例")
    print("=" * 60)
    
    # 模拟用户ID和知识库名称
    user_id = str(uuid.uuid4())
    kb_name = "技术文档库"
    
    print(f"\n1. 基本信息")
    print("-" * 60)
    print(f"用户ID: {user_id}")
    print(f"知识库名称: {kb_name}")
    
    # ========== 创建知识库 ==========
    print("\n2. 创建知识库")
    print("-" * 60)
    
    kb_config = {
        "user_id": user_id,
        "knowledge_base_name": kb_name,
        "knowledge_base_description": "存储技术文档和API说明",
        "vector_store_type": "faiss",  # 或 "milvus"
        "embed_model": "bge-large-zh-v1.5"
    }
    
    print("知识库配置:")
    for key, value in kb_config.items():
        print(f"  - {key}: {value}")
    
    print("\n调用 API: POST /api/knowledge_base/create")
    print("✓ 知识库创建成功")
    print("✓ 创建文档存储目录")
    print("✓ 初始化向量数据库索引")
    
    # ========== 上传文档 ==========
    print("\n3. 上传文档到知识库")
    print("-" * 60)
    
    files = [
        {"name": "Python入门教程.pdf", "size": "2.3 MB"},
        {"name": "FastAPI框架文档.md", "size": "1.1 MB"},
        {"name": "数据库设计规范.txt", "size": "0.5 MB"}
    ]
    
    for file_info in files:
        print(f"\n上传文件: {file_info['name']} ({file_info['size']})")
        print("  步骤1: 保存文件到磁盘")
        print("  步骤2: 加载文档内容")
        
        if file_info['name'].endswith('.pdf'):
            print("    - 使用 UnstructuredPDFLoader")
        elif file_info['name'].endswith('.md'):
            print("    - 使用 UnstructuredMarkdownLoader")
        else:
            print("    - 使用 TextLoader")
        
        print("  步骤3: 文本切分 (chunk_size=250, overlap=50)")
        
        # 模拟文档切分结果
        docs_count = 15 if file_info['name'].endswith('.pdf') else 8
        print(f"    - 切分为 {docs_count} 个文档块")
        
        print("  步骤4: 文档向量化")
        print(f"    - 使用嵌入模型: {kb_config['embed_model']}")
        print(f"    - 生成 {docs_count} 个向量")
        
        print("  步骤5: 添加到向量数据库")
        print(f"    - 向量库类型: {kb_config['vector_store_type']}")
        
        print("  步骤6: 更新元数据")
        print(f"    ✓ 文件 {file_info['name']} 添加成功")
    
    # ========== 列出知识库文件 ==========
    print("\n4. 列出知识库文件")
    print("-" * 60)
    
    print(f"查询知识库 '{kb_name}' 的文件列表")
    print("调用 API: GET /api/knowledge_base/files")
    
    print(f"\n✓ 知识库共有 {len(files)} 个文件:")
    for i, file_info in enumerate(files, 1):
        print(f"  [{i}] {file_info['name']} - {file_info['size']}")
    
    # ========== 向量检索 ==========
    print("\n5. 向量检索")
    print("-" * 60)
    
    query = "如何使用FastAPI创建API接口？"
    print(f"查询问题: {query}")
    
    print("\n检索流程:")
    print("  步骤1: 问题向量化")
    print(f"    - 使用嵌入模型: {kb_config['embed_model']}")
    
    print("  步骤2: 向量相似度搜索")
    print("    - top_k: 5")
    print("    - score_threshold: 0.5")
    
    # 模拟检索结果
    search_results = [
        {
            "content": "FastAPI是一个现代、快速的Web框架，用于构建API...",
            "score": 0.89,
            "source": "FastAPI框架文档.md",
            "page": 1
        },
        {
            "content": "创建API接口的基本步骤：1. 导入FastAPI 2. 创建app实例...",
            "score": 0.85,
            "source": "FastAPI框架文档.md",
            "page": 3
        },
        {
            "content": "路由装饰器的使用：@app.get() @app.post()...",
            "score": 0.78,
            "source": "FastAPI框架文档.md",
            "page": 5
        }
    ]
    
    print(f"\n  ✓ 找到 {len(search_results)} 个相关文档块:")
    for i, result in enumerate(search_results, 1):
        print(f"\n  [{i}] 相似度: {result['score']:.2f}")
        print(f"      来源: {result['source']} (第{result['page']}页)")
        print(f"      内容: {result['content'][:60]}...")
    
    # ========== Reranker重排序 ==========
    print("\n6. Reranker重排序（可选）")
    print("-" * 60)
    
    print("Reranker配置:")
    print("  - 模型: bge-reranker-large")
    print("  - top_n: 3")
    print("  - max_length: 512")
    
    print("\n重排序流程:")
    print("  步骤1: 使用Cross-Encoder计算query和doc的相关性")
    print("  步骤2: 重新排序并选择Top-3")
    
    reranked_results = search_results[:3]
    print(f"\n  ✓ 重排序后Top-3:")
    for i, result in enumerate(reranked_results, 1):
        print(f"  [{i}] {result['source']} - 相似度: {result['score']:.2f}")
    
    # ========== 知识库问答 ==========
    print("\n7. 知识库问答")
    print("-" * 60)
    
    print(f"问题: {query}")
    print(f"知识库: {kb_name}")
    
    print("\n问答流程:")
    print("  步骤1: 向量检索获取相关文档")
    print("  步骤2: （可选）Reranker重排序")
    print("  步骤3: 构建上下文Prompt")
    
    context = "\n\n".join([r['content'] for r in reranked_results])
    print(f"    - 上下文长度: {len(context)} 字符")
    
    print("  步骤4: 加载对话历史（支持多轮问答）")
    print("    - message_limit: 10")
    print("    - max_token_limit: 2000")
    
    print("  步骤5: 调用LLM生成回答")
    print("    - 模型: ChatGLM3-6b")
    print("    - 温度: 0.7")
    
    answer = """基于提供的文档，使用FastAPI创建API接口的步骤如下：

1. 首先安装FastAPI：
   pip install fastapi uvicorn

2. 创建基本的API应用：
   from fastapi import FastAPI
   app = FastAPI()

3. 使用装饰器定义路由：
   @app.get("/")
   def read_root():
       return {"message": "Hello World"}

4. 运行应用：
   uvicorn main:app --reload

这样就创建了一个简单的API接口。"""
    
    print("\n  ✓ 生成回答:")
    print("  " + "\n  ".join(answer.split("\n")))
    
    # ========== 获取用户知识库列表 ==========
    print("\n8. 获取用户知识库列表")
    print("-" * 60)
    
    print(f"查询用户 {user_id[:8]}... 的知识库")
    print("调用 API: GET /api/knowledge_base/list?user_id={user_id}")
    
    kb_list = [
        {"name": kb_name, "file_count": 3, "vs_type": "faiss"},
        {"name": "产品文档库", "file_count": 5, "vs_type": "faiss"}
    ]
    
    print(f"\n✓ 找到 {len(kb_list)} 个知识库:")
    for i, kb in enumerate(kb_list, 1):
        print(f"  [{i}] {kb['name']}")
        print(f"      - 文件数: {kb['file_count']}")
        print(f"      - 向量库: {kb['vs_type']}")
    
    # ========== 删除知识库 ==========
    print("\n9. 删除知识库")
    print("-" * 60)
    
    print(f"删除知识库 '{kb_name}'")
    print("调用 API: DELETE /api/knowledge_base/{kb_name}")
    
    print("\n删除流程:")
    print("  步骤1: 删除向量数据库索引")
    print("  步骤2: 删除文档文件")
    print("  步骤3: 删除数据库记录")
    
    print("\n✓ 知识库删除成功")
    
    print("\n" + "=" * 60)
    print("示例执行完成")
    print("=" * 60)


# ========== 高级用例 ==========
def advanced_usage_tips():
    """高级使用技巧"""
    
    print("\n\n高级使用技巧:")
    print("=" * 60)
    
    print("\n1. 向量库选择")
    print("   - Faiss: 适合中小规模（<100万文档），本地部署")
    print("   - Milvus: 适合大规模（>100万文档），分布式部署")
    
    print("\n2. 嵌入模型选择")
    print("   - 中文: bge-large-zh-v1.5, text2vec-large-chinese")
    print("   - 英文: bge-large-en-v1.5, OpenAI ada-002")
    print("   - 多语言: bge-m3, multilingual-e5-large")
    
    print("\n3. 文档切分策略")
    print("   - chunk_size: 250-500字符（中文）")
    print("   - chunk_overlap: 10%-20% of chunk_size")
    print("   - 按段落和句子智能切分")
    
    print("\n4. 检索参数调优")
    print("   - top_k: 5-10（召回阶段）")
    print("   - score_threshold: 0.3-0.7（根据效果调整）")
    print("   - rerank_top_k: 3-5（精排阶段）")
    
    print("\n5. 性能优化")
    print("   - 批量向量化（batch_size=32）")
    print("   - 使用GPU加速")
    print("   - 工厂模式缓存服务实例")
    print("   - 异步处理提升并发")
    
    print("\n6. 质量提升")
    print("   - 启用Reranker提升Top-3精度")
    print("   - 中文标题增强")
    print("   - 问题改写和扩展")
    print("   - Hybrid Search（向量+关键词）")


# ========== 代码示例 ==========
def code_examples():
    """实际代码示例"""
    
    print("\n\n实际代码示例:")
    print("=" * 60)
    
    print("\n1. 创建知识库（FastAPI）")
    print("-" * 60)
    print("""
from knowledge_base_access.repository.knowledge_base_repository import create_knowledge_base
from knowledge_base_access.models.knowledge_base_model import CreateKnowledgeBaseRequest

@app.post("/api/knowledge_base/create")
async def create_kb(
    request: CreateKnowledgeBaseRequest,
    session: AsyncSession = Depends(get_async_db)
):
    result = await create_knowledge_base(request, session)
    return result
""")
    
    print("\n2. 添加文档到知识库")
    print("-" * 60)
    print("""
from knowledge_base_access.kb_service.base import KBServiceFactory
from knowledge_base_access.utils import KnowledgeFile

# 获取知识库服务
kb_service = await KBServiceFactory.get_service_by_name(kb_name)

# 加载文档
kb_file = KnowledgeFile(
    filename="document.pdf",
    knowledge_base_name=kb_name
)
docs = kb_file.file2text()

# 添加到向量库
await kb_service.add_doc(kb_file, docs)
""")
    
    print("\n3. 向量检索")
    print("-" * 60)
    print("""
from knowledge_base_access.kb_service.base import search_docs

# 基础检索
docs = await search_docs(
    query="如何使用FastAPI？",
    knowledge_base_name="技术文档库",
    top_k=5,
    score_threshold=0.5
)

# 带Reranker的检索
if USE_RERANKER:
    reranker = LangchainReranker(top_n=3, ...)
    docs = reranker.compress_documents(documents=docs, query=query)

for doc, score in docs:
    print(f"Score: {score}, Content: {doc.page_content[:100]}")
""")
    
    print("\n4. 知识库问答（集成到对话）")
    print("-" * 60)
    print("""
from knowledge_base_access.kb_service.base import KBServiceFactory
from session_management.memory.conversation_db_buffer_memory import ConversationBufferDBMemory

async def knowledge_base_chat(query, conversation_id, kb_name):
    # 1. 检索相关文档
    docs = await search_docs(
        query=query,
        knowledge_base_name=kb_name,
        top_k=5
    )
    
    # 2. 构建上下文
    context = "\\n\\n".join([doc.page_content for doc in docs])
    
    # 3. 加载对话历史
    memory = ConversationBufferDBMemory(
        conversation_id=conversation_id,
        llm=model,
        chat_type="knowledge_base_chat",
        message_limit=10
    )
    
    # 4. 生成回答
    prompt = f"基于以下上下文回答问题：\\n{context}\\n\\n问题：{query}"
    chain = LLMChain(prompt=prompt, llm=model, memory=memory)
    
    async for token in chain.astream({"input": query}):
        yield token
""")


if __name__ == "__main__":
    # 运行主示例
    asyncio.run(knowledge_base_example())
    
    # 显示高级用法
    advanced_usage_tips()
    
    # 显示代码示例
    code_examples()
