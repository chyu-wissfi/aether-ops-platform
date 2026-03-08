"""
@Time: 2026/3/8
@Author: chyu.wissfi@gmail.com
@Description: ...
"""

from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class SQLAlchemy(_SQLAlchemy):
    """
    重写Flask-SQLAlchemy中的核心类，实现自动提交
    """
    @contextmanager
    def auto_commit(self):
        """
        上下文管理器，自动提交数据库变更
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e