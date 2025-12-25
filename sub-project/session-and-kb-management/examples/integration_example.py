"""
会话管理和知识库访问集成示例

本示例展示如何将会话管理和知识库访问两个模块集成在一起，
实现完整的知识库问答功能，并支持多轮对话。
"""

import asyncio
import uuid
from datetime import datetime


async def integrated_example():
    """集成示例：完整的知识库多轮问答流程"""
    
    print("=" * 70)
    print("会话管理 + 知识库访问 集成示例")
    print("=" * 70)
    
    # ========== 初始化 ==========
    print("\n【步骤1】初始化用户和知识库")
    print("-" * 70)
    
    user_id = str(uuid.uuid4())
    kb_name = "Python编程知识库"
    
    print(f"用户ID: {user_id[:8]}...")
    print(f"知识库名称: {kb_name}")
    
    # ========== 创建知识库 ==========
    print("\n【步骤2】创建知识库")
    print("-" * 70)
    
    kb_config = {
        "user_id": user_id,
        "knowledge_base_name": kb_name,
        "knowledge_base_description": "Python编程相关知识和最佳实践",
        "vector_store_type": "faiss",
        "embed_model": "bge-large-zh-v1.5"
    }
    
    print("知识库配置:")
    for key, value in kb_config.items():
        print(f"  {key}: {value}")
    
    print("\n✓ 知识库创建成功")
    print("✓ 向量数据库初始化完成")
    
    # ========== 上传文档 ==========
    print("\n【步骤3】上传文档到知识库")
    print("-" * 70)
    
    documents = [
        "Python基础教程.pdf",
        "FastAPI开发指南.md",
        "异步编程最佳实践.md"
    ]
    
    for doc_name in documents:
        print(f"  • 上传 {doc_name}")
    
    print("\n✓ 共上传 3 个文档")
    print("✓ 文档切分和向量化完成")
    print("✓ 向量索引构建完成")
    
    # ========== 创建对话会话 ==========
    print("\n【步骤4】创建知识库问答会话")
    print("-" * 70)
    
    conversation_data = {
        "user_id": user_id,
        "name": "新对话",
        "chat_type": "knowledge_base_chat"
    }
    
    conversation_id = str(uuid.uuid4())
    print(f"会话ID: {conversation_id[:8]}...")
    print(f"会话类型: knowledge_base_chat")
    print("\n✓ 会话创建成功")
    
    # ========== 第一轮问答 ==========
    print("\n【步骤5】第一轮问答")
    print("=" * 70)
    
    query_1 = "FastAPI中如何创建异步路由？"
    print(f"\n👤 用户问题: {query_1}")
    print("\n🔍 处理流程:")
    
    # 5.1 创建消息记录
    message_id_1 = str(uuid.uuid4())
    print(f"  1. 创建消息记录 (ID: {message_id_1[:8]}...)")
    
    # 5.2 向量检索
    print(f"  2. 在知识库 '{kb_name}' 中检索相关文档")
    print("     - 查询向量化")
    print("     - 相似度搜索 (top_k=5)")
    
    # 模拟检索结果
    retrieved_docs = [
        {
            "content": "FastAPI支持异步路由定义，使用async def声明路由函数...",
            "score": 0.92,
            "source": "FastAPI开发指南.md",
            "page": 5
        },
        {
            "content": "异步路由示例：@app.get('/items') async def read_items()...",
            "score": 0.87,
            "source": "FastAPI开发指南.md",
            "page": 6
        },
        {
            "content": "使用asyncio和await处理异步操作，提升性能...",
            "score": 0.81,
            "source": "异步编程最佳实践.md",
            "page": 3
        }
    ]
    
    print(f"     - ✓ 检索到 {len(retrieved_docs)} 个相关文档块")
    
    for i, doc in enumerate(retrieved_docs, 1):
        print(f"\n     [{i}] 相似度: {doc['score']:.2f}")
        print(f"         来源: {doc['source']} (第{doc['page']}页)")
        print(f"         内容片段: {doc['content'][:50]}...")
    
    # 5.3 构建上下文
    print("\n  3. 构建Prompt上下文")
    context_1 = "\n\n".join([doc['content'] for doc in retrieved_docs])
    print(f"     - 上下文总长度: {len(context_1)} 字符")
    
    # 5.4 加载对话历史
    print("\n  4. 加载对话历史")
    print("     - conversation_id: " + conversation_id[:8] + "...")
    print("     - message_limit: 10")
    print("     - max_token_limit: 2000")
    print("     - 当前历史消息数: 0 (首轮对话)")
    
    # 5.5 生成回答
    print("\n  5. 调用LLM生成回答")
    print("     - 模型: ChatGLM3-6b")
    print("     - 温度: 0.7")
    print("     - 流式输出: 是")
    
    response_1 = """在FastAPI中创建异步路由非常简单，主要有以下步骤：

1. 使用 async def 声明路由函数：
```python
@app.get("/items")
async def read_items():
    # 异步操作
    result = await some_async_operation()
    return result
```

2. 在路由函数内部使用 await 调用异步操作：
   - 数据库查询
   - HTTP请求
   - 文件I/O等

3. FastAPI会自动处理异步上下文，确保并发性能。

优势：
- 提升并发处理能力
- 更好的资源利用
- 适合I/O密集型任务

这样就可以充分利用异步编程的优势！"""
    
    print("\n🤖 AI回答:")
    print(response_1)
    
    # 5.6 更新消息记录
    print("\n  6. 更新消息记录")
    print(f"     - 将回答写入message表")
    print(f"     - 更新会话名称为: '{query_1}'")
    print("\n✓ 第一轮问答完成")
    
    # ========== 第二轮问答 ==========
    print("\n【步骤6】第二轮问答（利用对话历史）")
    print("=" * 70)
    
    query_2 = "那如何处理异步数据库查询呢？"
    print(f"\n👤 用户问题: {query_2}")
    print("\n🔍 处理流程:")
    
    # 6.1 创建消息记录
    message_id_2 = str(uuid.uuid4())
    print(f"  1. 创建消息记录 (ID: {message_id_2[:8]}...)")
    
    # 6.2 向量检索（基于新问题）
    print(f"  2. 在知识库 '{kb_name}' 中检索相关文档")
    
    retrieved_docs_2 = [
        {
            "content": "使用SQLAlchemy的异步引擎进行数据库操作...",
            "score": 0.89,
            "source": "Python基础教程.pdf",
            "page": 120
        },
        {
            "content": "asyncio与数据库连接池的配合使用...",
            "score": 0.84,
            "source": "异步编程最佳实践.md",
            "page": 8
        }
    ]
    
    print(f"     - ✓ 检索到 {len(retrieved_docs_2)} 个相关文档块")
    
    # 6.3 加载对话历史（包含上一轮）
    print("\n  3. 加载对话历史")
    print("     - 当前历史消息数: 2 (1轮对话)")
    print("     - 历史摘要:")
    print(f"       [1] 用户: {query_1[:30]}...")
    print(f"           AI: {response_1[:50]}...")
    print(f"       [2] 用户: {query_2[:30]}...")
    
    # 6.4 上下文增强
    print("\n  4. 上下文增强")
    print("     - 检索到的文档上下文")
    print("     - 对话历史上下文")
    print("     - 当前问题")
    
    # 6.5 生成回答
    print("\n  5. 生成回答（理解上下文）")
    
    response_2 = """基于我们刚才讨论的异步路由，处理异步数据库查询的方法如下：

1. 使用SQLAlchemy的异步引擎：
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("mysql+aiomysql://...")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(User).filter(User.id == user_id)
        )
        user = result.scalars().first()
        return user
```

2. 关键点：
   - 使用 create_async_engine 创建异步引擎
   - 使用 AsyncSession 管理会话
   - 使用 await 执行查询

3. 配置连接池提升性能：
```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```

这样就能在异步路由中高效地处理数据库查询了！"""
    
    print("\n🤖 AI回答:")
    print(response_2)
    
    print("\n✓ 第二轮问答完成")
    print("✓ AI成功理解了上下文关系（'那'字指代前文）")
    
    # ========== 查看会话历史 ==========
    print("\n【步骤7】查看完整会话历史")
    print("=" * 70)
    
    print(f"\n会话名称: {query_1}")
    print(f"会话类型: knowledge_base_chat")
    print(f"消息数量: 4 (2轮对话)")
    print(f"\n对话记录:")
    
    messages = [
        {"role": "user", "content": query_1},
        {"role": "assistant", "content": response_1},
        {"role": "user", "content": query_2},
        {"role": "assistant", "content": response_2}
    ]
    
    for i, msg in enumerate(messages, 1):
        role = "👤 用户" if msg["role"] == "user" else "🤖 AI"
        print(f"\n[{i}] {role}:")
        print(f"    {msg['content'][:60]}...")
    
    # ========== 系统统计 ==========
    print("\n【步骤8】系统统计信息")
    print("=" * 70)
    
    print(f"\n用户统计:")
    print(f"  - 知识库数量: 1")
    print(f"  - 会话数量: 1")
    print(f"  - 消息数量: 4")
    
    print(f"\n知识库统计:")
    print(f"  - 名称: {kb_name}")
    print(f"  - 文档数: 3")
    print(f"  - 文档块数: ~45 (估算)")
    print(f"  - 向量维度: 1024")
    
    print(f"\n性能指标:")
    print(f"  - 向量检索耗时: ~50ms")
    print(f"  - LLM生成耗时: ~2.5s")
    print(f"  - 总响应时间: ~3s")
    
    # ========== 总结 ==========
    print("\n" + "=" * 70)
    print("集成示例执行完成")
    print("=" * 70)
    
    print("\n✅ 成功演示的功能:")
    print("  1. 创建知识库并上传文档")
    print("  2. 创建知识库问答会话")
    print("  3. 向量检索相关文档")
    print("  4. 生成基于检索的回答")
    print("  5. 多轮对话上下文理解")
    print("  6. 完整的会话历史管理")


# ========== 架构说明 ==========
def architecture_explanation():
    """架构说明"""
    
    print("\n\n系统架构说明:")
    print("=" * 70)
    
    print("\n1. 数据流向")
    print("-" * 70)
    print("""
用户问题
    ↓
[会话管理] 创建消息记录
    ↓
[知识库访问] 向量检索
    ↓
[知识库访问] 文档召回
    ↓
[会话管理] 加载对话历史
    ↓
[LLM] 生成回答 (Prompt = 上下文 + 历史 + 问题)
    ↓
[会话管理] 更新消息记录
    ↓
返回回答
""")
    
    print("\n2. 模块职责")
    print("-" * 70)
    print("""
会话管理模块:
  • 管理用户、会话、消息的生命周期
  • 提供对话历史缓冲
  • 与LangChain集成
  • 支持多轮对话

知识库访问模块:
  • 管理知识库和文档
  • 文档加载和向量化
  • 向量检索和重排序
  • 支持多种向量数据库
""")
    
    print("\n3. 集成要点")
    print("-" * 70)
    print("""
• 使用同一个user_id关联会话和知识库
• conversation_id + knowledge_base_name 实现知识库问答
• ConversationBufferDBMemory提供历史上下文
• 检索结果 + 对话历史 = 完整的Prompt上下文
• 流式返回提升用户体验
""")


# ========== 最佳实践 ==========
def best_practices():
    """最佳实践建议"""
    
    print("\n\n最佳实践建议:")
    print("=" * 70)
    
    print("\n1. 会话管理")
    print("-" * 70)
    print("  • 限制历史消息数量（10-20条）")
    print("  • 控制Token总数（2000-4000）")
    print("  • 不同chat_type独立管理")
    print("  • 定期清理过期会话")
    
    print("\n2. 知识库访问")
    print("-" * 70)
    print("  • 合理设置chunk_size（250-500字符）")
    print("  • 使用Reranker提升精度")
    print("  • 启用批量向量化")
    print("  • 缓存高频查询结果")
    
    print("\n3. 性能优化")
    print("-" * 70)
    print("  • 数据库连接池配置")
    print("  • 向量库服务实例缓存")
    print("  • 异步处理提升并发")
    print("  • GPU加速向量计算")
    
    print("\n4. 用户体验")
    print("-" * 70)
    print("  • 流式返回回答")
    print("  • 智能会话命名")
    print("  • 展示检索来源")
    print("  • 支持用户反馈")


if __name__ == "__main__":
    # 运行集成示例
    asyncio.run(integrated_example())
    
    # 显示架构说明
    architecture_explanation()
    
    # 显示最佳实践
    best_practices()
