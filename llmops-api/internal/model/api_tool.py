"""
@Time: 2026/3/19
@Author: chyu.wissfi@gmail.com
@Description: API 工具提供商模型
"""


from sqlalchemy import (
    Column,
    UUID,
    String,
    DateTime,
    PrimaryKeyConstraint,
    UniqueConstraint,
    Index,
    text,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from internal.extension.database_extension import db


class ApiToolProvider(db.Model):
    """API 工具提供商模型"""
    __tablename__ = "api_tool_provider"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_api_tool_provider_id"),
        # 用户需求：account_id + name 是索引 (通常业务场景下为联合唯一索引)
        # UniqueConstraint("account_id", "name", name="uk_api_tool_provider_account_id_name"),
        # Index("idx_api_tool_provider_account_id", "account_id")
    )
    id = Column(UUID, nullable=False, server_default=text('uuid_generate_v4()'))
    account_id = Column(UUID, nullable=False)
    # 提供者名称
    name = Column(String(255), nullable=False, server_default=text("''::character varying"))
    # 提供者图标 URL 地址
    icon = Column(String(255), nullable=False, server_default=text("''::character varying"))
    # 提供者描述 (内容较长，使用 Text 类型)
    description = Column(Text, nullable=False, server_default=text("''::text"))
    # 接口的 openapi 规范描述 (JSON 类型统一使用 JSONB)
    openapi_schema = Column(JSONB, nullable=False)
    # api 接口需要 headers 请求头数据 (JSON 类型统一使用 JSONB)
    headers = Column(JSONB, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP(0)'),
        server_onupdate=text('CURRENT_TIMESTAMP(0)')
    )
    created_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP(0)'))

    @property
    def tools(self) -> list["ApiTool"]:
        """只读属性，返回当前提供者关联的所有工具"""
        return db.session.query(ApiTool).filter(ApiTool.provider_id == self.id).all()


class ApiTool(db.Model):
    """API工具表模型"""
    __tablename__ = "api_tool"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_api_tool_id"),
        # Index("idx_api_tool_account_id", "account_id"),
        # Index("idx_api_tool_provider_id_name", "provider_id", "name")
    )

    id = Column(UUID, nullable=False, server_default=text('uuid_generate_v4()'))
    account_id = Column(UUID, nullable=False)
    provider_id = Column(UUID, nullable=False)
    name = Column(String(255), nullable=False, server_default=text("''::character varying"))
    description = Column(Text, nullable=False, server_default=text("''::text"))
    url = Column(String(255), nullable=False, server_default=text("''::character varying"))
    method = Column(String(255), nullable=False, server_default=text("''::character varying"))
    parameters = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP(0)'), server_onupdate=text('CURRENT_TIMESTAMP(0)'))
    created_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP(0)'))

    @property
    def provider(self) -> "ApiToolProvider":
        """只读属性，返回当前工具关联/归属的工具提供者信息"""
        return db.session.query(ApiToolProvider).get(self.provider_id)