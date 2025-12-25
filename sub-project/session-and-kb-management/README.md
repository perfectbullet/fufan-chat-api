# 会话管理和知识库访问参考实现

本项目从 [FuFan Chat API](https://github.com/perfectbullet/fufan-chat-api) 中提取了会话管理和知识库访问的核心代码，作为一个独立的参考实现，供其他项目借鉴使用。

## 项目概述

该参考实现包含两个核心模块：

1. **会话管理（Session Management）**：基于MySQL的多用户、多会话、多轮对话管理系统
2. **知识库访问（Knowledge Base Access）**：基于RAG架构的私有知识库问答系统

## 特性亮点

### 会话管理
- ✅ 多用户隔离，数据安全
- ✅ 支持多种对话类型（普通对话、知识库问答、Agent对话）
- ✅ 基于数据库的对话历史缓冲
- ✅ 智能Token管理，自动截断超长上下文
- ✅ 与LangChain无缝集成
- ✅ 异步数据库操作，高并发支持

### 知识库访问
- ✅ 支持多种向量数据库（Faiss、Milvus）
- ✅ 支持多种文档格式（PDF、Markdown、TXT等）
- ✅ 工厂模式+抽象基类，易于扩展
- ✅ 智能文档切分和向量化
- ✅ 向量检索 + Reranker精排
- ✅ 用户级数据隔离

## 技术栈

- **Web框架**: FastAPI
- **数据库ORM**: SQLAlchemy (异步)
- **关系型数据库**: MySQL 5.7+
- **向量数据库**: Faiss / Milvus 2.3.7+
- **嵌入模型**: BGE-large-zh-v1.5 (或其他兼容模型)
- **LLM框架**: LangChain
- **文档处理**: Unstructured, LangChain DocumentLoaders
- **重排序模型**: BGE Reranker

## 目录结构

```
sub-project/session-and-kb-management/
├── session_management/          # 会话管理模块
│   ├── models/                 # 数据模型
│   │   ├── user_model.py
│   │   ├── conversation_model.py
│   │   └── message_model.py
│   ├── repository/             # 数据访问层
│   │   ├── conversation_repository.py
│   │   └── message_repository.py
│   ├── memory/                 # 内存管理
│   │   └── conversation_db_buffer_memory.py
│   └── session.py              # 会话管理工具
├── knowledge_base_access/       # 知识库访问模块
│   ├── models/                 # 数据模型
│   │   ├── knowledge_base_model.py
│   │   └── knowledge_file_model.py
│   ├── repository/             # 数据访问层
│   │   └── knowledge_base_repository.py
│   ├── kb_service/             # 知识库服务
│   │   ├── base.py            # 抽象基类
│   │   ├── faiss_kb_service.py (参考原项目)
│   │   └── milvus_kb_service.py (参考原项目)
│   └── utils.py                # 工具函数 (参考原项目)
├── docs/                        # 文档
│   ├── 01_会话管理设计分析.md
│   ├── 02_知识库访问设计分析.md
│   └── 03_实现文档.md
├── examples/                    # 使用示例
│   ├── session_example.py
│   └── knowledge_base_example.py
├── requirements.txt             # 依赖列表
└── README.md                    # 本文件
```

## 快速开始

### 1. 环境要求

- Python 3.10+
- MySQL 5.7+ 或 8.0+
- （可选）Milvus 2.3.7+（用于大规模知识库）
- 4GB+ RAM
- （推荐）CUDA GPU（用于加速向量计算）

### 2. 安装依赖

```bash
cd sub-project/session-and-kb-management
pip install -r requirements.txt
```

主要依赖：
- fastapi
- sqlalchemy[asyncio]
- aiomysql
- langchain
- langchain-community
- faiss-cpu (或 faiss-gpu)
- pymilvus (如果使用Milvus)

### 3. 数据库初始化

创建MySQL数据库并执行表结构初始化：

```sql
CREATE DATABASE fufan_chat DEFAULT CHARACTER SET utf8mb4;
```

然后参考 `docs/03_实现文档.md` 中的表结构创建SQL。

### 4. 配置

配置数据库连接和向量库参数（参考原项目的配置文件）：

```python
# database.py
DATABASE_URL = "mysql+aiomysql://user:password@localhost:3306/fufan_chat"

# config.py
EMBEDDING_MODEL = "bge-large-zh-v1.5"
VECTOR_SEARCH_TOP_K = 5
SCORE_THRESHOLD = 0.5
```

### 5. 运行示例

```bash
# 会话管理示例
python examples/session_example.py

# 知识库访问示例
python examples/knowledge_base_example.py
```

## 核心功能

### 会话管理

#### 创建会话

```python
from session_management.repository.conversation_repository import create_conversation

conversation_data = {
    "user_id": "user-uuid",
    "name": "新对话",
    "chat_type": "chat"
}

result = await create_conversation(conversation_data, session)
conversation_id = result["id"]
```

#### 添加消息

```python
from session_management.repository.message_repository import add_message_to_db

message_id = await add_message_to_db(
    query="什么是人工智能？",
    conversation_id=conversation_id,
    prompt_name="chat",
    response="",
    metadata={}
)
```

#### 加载对话历史

```python
from session_management.memory.conversation_db_buffer_memory import ConversationBufferDBMemory

memory = ConversationBufferDBMemory(
    conversation_id=conversation_id,
    llm=model,
    chat_type="chat",
    message_limit=10,
    max_token_limit=2000
)

# 集成到LangChain
chain = LLMChain(prompt=prompt, llm=model, memory=memory)
```

### 知识库访问

#### 创建知识库

```python
from knowledge_base_access.repository.knowledge_base_repository import create_knowledge_base

kb_config = {
    "user_id": "user-uuid",
    "knowledge_base_name": "技术文档库",
    "knowledge_base_description": "存储技术文档",
    "vector_store_type": "faiss",
    "embed_model": "bge-large-zh-v1.5"
}

result = await create_knowledge_base(kb_config, session)
```

#### 添加文档

```python
from knowledge_base_access.kb_service.base import KBServiceFactory
from knowledge_base_access.utils import KnowledgeFile

# 获取知识库服务
kb_service = await KBServiceFactory.get_service_by_name(kb_name)

# 加载并添加文档
kb_file = KnowledgeFile(filename="document.pdf", knowledge_base_name=kb_name)
docs = kb_file.file2text()
await kb_service.add_doc(kb_file, docs)
```

#### 向量检索

```python
from knowledge_base_access.kb_service.base import search_docs

docs = await search_docs(
    query="如何使用FastAPI？",
    knowledge_base_name="技术文档库",
    top_k=5,
    score_threshold=0.5
)

for doc, score in docs:
    print(f"Score: {score}, Content: {doc.page_content[:100]}")
```

#### 知识库问答

```python
async def knowledge_base_chat(query, conversation_id, kb_name):
    # 1. 检索相关文档
    docs = await search_docs(query=query, knowledge_base_name=kb_name, top_k=5)
    
    # 2. 构建上下文
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # 3. 加载对话历史
    memory = ConversationBufferDBMemory(
        conversation_id=conversation_id,
        llm=model,
        chat_type="knowledge_base_chat",
        message_limit=10
    )
    
    # 4. 生成回答
    prompt = f"基于以下上下文回答问题：\n{context}\n\n问题：{query}"
    chain = LLMChain(prompt=prompt, llm=model, memory=memory)
    
    result = await chain.acall({"input": query})
    return result
```

## 文档

详细的设计分析和实现文档位于 `docs/` 目录：

1. **[会话管理设计分析](docs/01_会话管理设计分析.md)**
   - 设计理念
   - 数据模型
   - 核心功能实现
   - 内存管理机制

2. **[知识库访问设计分析](docs/02_知识库访问设计分析.md)**
   - 架构设计
   - 向量库服务
   - 文档处理流程
   - 检索和重排序

3. **[实现文档](docs/03_实现文档.md)**
   - 技术栈
   - 数据库设计
   - 配置说明
   - 部署指南
   - 性能优化

## 数据库设计

### 核心表结构

- **user**: 用户表
- **conversation**: 会话表
- **message**: 消息表
- **knowledge_base**: 知识库表
- **knowledge_file**: 知识文件表
- **file_doc**: 文档向量映射表

详细的表结构和索引设计请参考 `docs/03_实现文档.md`。

## 架构特点

### 会话管理架构

```
用户 (User)
  ├── 会话 (Conversation)
  │   ├── 消息 (Message)
  │   ├── 消息 (Message)
  │   └── ...
  └── 会话 (Conversation)
      └── ...
```

- 三层模型：User → Conversation → Message
- 异步数据库操作
- 装饰器模式简化会话管理
- 基于数据库的历史缓冲

### 知识库访问架构

```
用户 (User)
  ├── 知识库 (KnowledgeBase)
  │   ├── 文件 (KnowledgeFile)
  │   │   └── 文档块 (Document Chunks) → 向量库
  │   └── 文件 (KnowledgeFile)
  │       └── ...
  └── 知识库 (KnowledgeBase)
      └── ...
```

- 三层存储：MySQL元数据 + 向量数据库 + 文件系统
- 工厂模式统一服务创建
- 抽象基类定义统一接口
- 支持多种向量库类型

## 最佳实践

### 会话管理

1. **历史记录限制**
   - message_limit: 10-20条
   - max_token_limit: 2000-4000
   - 根据模型上下文长度调整

2. **会话命名**
   - 首次提问自动命名
   - 支持用户手动修改

3. **多类型管理**
   - 不同chat_type独立管理
   - 便于统计和分析

### 知识库访问

1. **向量库选择**
   - 小规模（<100万）：Faiss
   - 大规模（>100万）：Milvus

2. **文档切分**
   - chunk_size: 250-500字符
   - chunk_overlap: 10%-20%
   - 按语义边界切分

3. **检索优化**
   - top_k: 5-10（召回）
   - score_threshold: 0.3-0.7
   - 启用Reranker提升Top-3精度

4. **嵌入模型**
   - 中文：bge-large-zh-v1.5
   - 英文：bge-large-en-v1.5
   - 多语言：bge-m3

## 性能优化

1. **数据库优化**
   - 连接池配置
   - 索引优化
   - 查询优化（避免N+1）

2. **向量检索优化**
   - 批量向量化
   - GPU加速
   - 服务实例缓存

3. **异步处理**
   - 全流程异步化
   - 提升并发能力

## 扩展建议

1. **新增向量库类型**
   - 继承KBService抽象基类
   - 实现抽象方法
   - 在工厂类中注册

2. **新增文档格式**
   - 实现对应的DocumentLoader
   - 在KnowledgeFile中添加处理逻辑

3. **新增对话类型**
   - 在chat_type中添加新类型
   - 实现对应的对话逻辑

## 许可证

本项目基于原项目 [FuFan Chat API](https://github.com/perfectbullet/fufan-chat-api) 提取，遵循原项目的开源许可证。

## 致谢

感谢 FuFan Chat API 项目团队的优秀工作，本参考实现基于该项目的核心代码整理而成。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 原项目仓库: https://github.com/perfectbullet/fufan-chat-api
- 提交Issue: https://github.com/perfectbullet/fufan-chat-api/issues

## 更新日志

### v1.0.0 (2025-12-25)

- ✅ 提取会话管理核心代码
- ✅ 提取知识库访问核心代码
- ✅ 编写完整的设计分析文档
- ✅ 编写实现文档
- ✅ 创建使用示例
- ✅ 整理项目结构

---

**注意**: 本项目为参考实现，实际使用时需要根据具体需求进行调整和优化。完整的实现请参考原项目 [FuFan Chat API](https://github.com/perfectbullet/fufan-chat-api)。
