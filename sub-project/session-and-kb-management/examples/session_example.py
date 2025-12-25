"""
会话管理使用示例

本示例展示如何使用会话管理模块进行用户会话的创建、查询、更新和删除操作。
"""

import asyncio
import uuid
from datetime import datetime


async def session_management_example():
    """会话管理完整示例"""
    
    print("=" * 60)
    print("会话管理使用示例")
    print("=" * 60)
    
    # 模拟用户ID
    user_id = str(uuid.uuid4())
    print(f"\n1. 模拟用户ID: {user_id}")
    
    # ========== 创建会话 ==========
    print("\n2. 创建新会话")
    print("-" * 60)
    
    # 创建普通对话会话
    conversation_data = {
        "user_id": user_id,
        "name": "新对话",
        "chat_type": "chat"
    }
    
    print(f"会话数据: {conversation_data}")
    print("调用 API: POST /api/conversation/create")
    
    # 模拟返回的会话ID
    conversation_id = str(uuid.uuid4())
    print(f"✓ 会话创建成功，会话ID: {conversation_id}")
    
    # ========== 添加消息 ==========
    print("\n3. 添加消息到会话")
    print("-" * 60)
    
    # 第一轮对话
    query1 = "什么是人工智能？"
    print(f"用户问题: {query1}")
    
    # 模拟添加消息到数据库
    message_id_1 = str(uuid.uuid4())
    response1 = "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统..."
    
    print(f"✓ 消息记录创建成功")
    print(f"  - Message ID: {message_id_1}")
    print(f"  - 会话自动命名为: '{query1}'")
    print(f"  - 回答: {response1[:50]}...")
    
    # 第二轮对话
    query2 = "它有哪些应用场景？"
    print(f"\n用户问题: {query2}")
    
    message_id_2 = str(uuid.uuid4())
    response2 = "人工智能的应用场景非常广泛，包括：1. 自然语言处理 2. 计算机视觉 3. 推荐系统..."
    
    print(f"✓ 消息记录创建成功")
    print(f"  - Message ID: {message_id_2}")
    print(f"  - 回答: {response2[:50]}...")
    
    # ========== 获取用户会话列表 ==========
    print("\n4. 获取用户会话列表")
    print("-" * 60)
    
    print(f"查询用户 {user_id[:8]}... 的会话")
    print("调用 API: GET /api/conversation/list?user_id={user_id}&chat_types=chat")
    
    # 模拟返回的会话列表
    conversations = [
        {
            "id": conversation_id,
            "name": query1,
            "chat_type": "chat",
            "create_time": datetime.now().isoformat()
        }
    ]
    
    print(f"✓ 找到 {len(conversations)} 个会话:")
    for conv in conversations:
        print(f"  - {conv['name'][:30]}... (ID: {conv['id'][:8]}...)")
    
    # ========== 获取会话消息历史 ==========
    print("\n5. 获取会话消息历史")
    print("-" * 60)
    
    print(f"查询会话 {conversation_id[:8]}... 的消息历史")
    print(f"调用 API: GET /api/conversation/messages/{conversation_id}")
    
    # 模拟返回的消息列表
    messages = [
        {
            "id": message_id_1,
            "query": query1,
            "response": response1,
            "create_time": datetime.now().isoformat()
        },
        {
            "id": message_id_2,
            "query": query2,
            "response": response2,
            "create_time": datetime.now().isoformat()
        }
    ]
    
    print(f"✓ 找到 {len(messages)} 条消息:")
    for i, msg in enumerate(messages, 1):
        print(f"\n  [{i}] 用户: {msg['query']}")
        print(f"      AI: {msg['response'][:50]}...")
    
    # ========== 更新会话名称 ==========
    print("\n6. 更新会话名称")
    print("-" * 60)
    
    new_name = "人工智能科普对话"
    print(f"新名称: {new_name}")
    print(f"调用 API: PUT /api/conversation/{conversation_id}")
    
    print(f"✓ 会话名称更新成功")
    
    # ========== 内存管理示例 ==========
    print("\n7. 对话历史内存管理")
    print("-" * 60)
    
    print("ConversationBufferDBMemory 配置:")
    print("  - conversation_id: " + conversation_id[:8] + "...")
    print("  - message_limit: 10")
    print("  - max_token_limit: 2000")
    print("  - chat_type: chat")
    
    print("\n✓ 从数据库加载最近10条消息")
    print("✓ 转换为LangChain消息格式")
    print("✓ 检查Token数量，自动截断超出部分")
    print(f"✓ 当前消息数: {len(messages)}, Token数: ~500")
    
    # ========== 删除会话 ==========
    print("\n8. 删除会话")
    print("-" * 60)
    
    print(f"删除会话 {conversation_id[:8]}...")
    print(f"调用 API: DELETE /api/conversation/{conversation_id}")
    
    print("✓ 会话删除成功")
    print("✓ 关联的所有消息也已删除")
    
    print("\n" + "=" * 60)
    print("示例执行完成")
    print("=" * 60)


# ========== 高级用例 ==========
def advanced_usage_tips():
    """高级使用技巧"""
    
    print("\n\n高级使用技巧:")
    print("=" * 60)
    
    print("\n1. 多类型会话管理")
    print("   - chat_type: 'chat' (普通对话)")
    print("   - chat_type: 'knowledge_base_chat' (知识库问答)")
    print("   - chat_type: 'agent_chat' (Agent问答)")
    print("   每种类型可独立管理历史记录")
    
    print("\n2. 历史记录限制策略")
    print("   - message_limit: 控制加载的消息数量")
    print("   - max_token_limit: 控制上下文Token总数")
    print("   - 智能截断: 优先保留最近的对话")
    
    print("\n3. 流式响应处理")
    print("   - 先创建消息记录（预分配ID）")
    print("   - 流式返回Token时附带message_id")
    print("   - 前端可以根据message_id更新UI")
    
    print("\n4. 会话命名策略")
    print("   - 首次提问自动命名")
    print("   - 支持用户手动修改")
    print("   - 提升用户体验")
    
    print("\n5. 元数据扩展")
    print("   - meta_data字段存储JSON")
    print("   - 可记录知识库ID、检索文档等")
    print("   - 支持未来功能扩展")
    
    print("\n6. 用户反馈机制")
    print("   - feedback_score: 用户评分（0-100）")
    print("   - feedback_reason: 评分理由")
    print("   - 用于模型优化和质量评估")


# ========== 代码示例 ==========
def code_examples():
    """实际代码示例"""
    
    print("\n\n实际代码示例:")
    print("=" * 60)
    
    print("\n1. 创建会话（FastAPI）")
    print("-" * 60)
    print("""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from session_management.repository.conversation_repository import create_conversation
from session_management.models.conversation_model import CreateConversationRequest

@app.post("/api/conversation/create")
async def create_new_conversation(
    request: CreateConversationRequest,
    session: AsyncSession = Depends(get_async_db)
):
    result = await create_conversation(request, session)
    return result
""")
    
    print("\n2. 添加消息（使用装饰器）")
    print("-" * 60)
    print("""
from session_management.repository.message_repository import add_message_to_db

# 使用装饰器自动管理数据库会话
@with_async_session
async def save_message(session, query, conversation_id):
    message_id = await add_message_to_db(
        session=session,
        query=query,
        conversation_id=conversation_id,
        prompt_name="chat",
        response="",
        metadata={}
    )
    return message_id

# 调用
message_id = await save_message(query="你好", conversation_id="xxx")
""")
    
    print("\n3. 加载对话历史（LangChain集成）")
    print("-" * 60)
    print("""
from session_management.memory.conversation_db_buffer_memory import ConversationBufferDBMemory
from langchain.chains import LLMChain

# 创建内存管理器
memory = ConversationBufferDBMemory(
    conversation_id=conversation_id,
    llm=model,
    chat_type="chat",
    message_limit=10,
    max_token_limit=2000
)

# 集成到LangChain
chain = LLMChain(
    prompt=prompt_template,
    llm=model,
    memory=memory
)

# 执行对话（自动加载历史）
result = await chain.acall({"input": query})
""")


if __name__ == "__main__":
    # 运行主示例
    asyncio.run(session_management_example())
    
    # 显示高级用法
    advanced_usage_tips()
    
    # 显示代码示例
    code_examples()
