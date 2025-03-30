from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, func, CHAR
from sqlalchemy.orm import relationship
from server.db.base import Base


class UserModel(Base):
    __tablename__ = 'user'
    __table_args__ = {
        "mysql_charset": "utf8mb4",  # 设置字符集
        "mysql_collate": "utf8mb4_unicode_ci"  # 设置排序规则
    }
    id = Column(CHAR(36), primary_key=True, comment='用户ID')
    username = Column(String(255), unique=True, comment='用户名')
    password_hash = Column(String(255), comment='密码的哈希值')
    # 可以添加更多用户相关的字段，如邮箱、电话等

    conversations = relationship('ConversationModel', back_populates='user')
    knowledge_bases = relationship('KnowledgeBaseModel', back_populates='user', cascade='all, delete-orphan')  # 更新关系

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}')>"
