"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: Config file
"""
import os
from typing import Any
from .default_congig import DEFAULT_CONFIG

def _get_env_var(key: str) -> Any:
    """
    从环境变量中获取配置值，若未设置则使用默认值
    """
    return os.environ.get(key, DEFAULT_CONFIG.get(key))

def _get_bool_env(key: str) -> bool:
    """
    从环境变量中获取布尔值配置，若未设置则使用默认值
    """
    value = _get_env_var(key)
    return value.lower() == 'true' if value is not None else False

class Config:
    """
    Config class
    """
    def __init__(self):
        # 关闭 WTF 的 CSRF保护
        self.WTF_CSRF_ENABLED = _get_bool_env('WTF_CSRF_ENABLED')
        # 数据库配置
        self.SQLALCHEMY_DATABASE_URI = _get_env_var('SQLALCHEMY_DATABASE_URI')
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': int(_get_env_var('SQLALCHEMY_POOL_SIZE')),
            'pool_recycle': int(_get_env_var('SQLALCHEMY_POOL_RECYCLE')),
        }
        self.SQLALCHEMY_ECHO = _get_bool_env('SQLALCHEMY_ECHO') 
