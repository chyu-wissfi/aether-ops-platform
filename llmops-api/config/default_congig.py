"""
@Time: 2026/3/8
@Author: chyu.wissfi@gmail.com
@Description: Default config file
"""
from typing import Any

# 应用默认配置
DEFAULT_CONFIG: dict[str, Any] = {
    # WTF 配置
    'WTF_CSRF_ENABLED': 'False',
    # SQLAlchemy 数据库配置
    'SQLALCHEMY_DATABASE_URI': "",
    'SQLALCHEMY_POOL_SIZE': 30,
    'SQLALCHEMY_POOL_RECYCLE': 3600,
    'SQLALCHEMY_ECHO': 'True',
}
