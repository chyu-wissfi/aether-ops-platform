"""
@Time: 2026/3/8
@Author: chyu.wissfi@gmail.com
@Description: ...
"""

from dataclasses import dataclass
from injector import inject
from pkg.sqlalchemy import SQLAlchemy
import uuid
from internal.model.app import App

@inject
@dataclass
class AppService:
    """
    AI 应用服务逻辑
    """
    db: SQLAlchemy

    def create_app(self) -> App:
        """
        创建 AI 应用
        """
        with self.db.auto_commit():
            app = App(
                account_id=uuid.uuid4(),
                name="测试机器人",
                icon="",
                description="这是一个简单的聊天机器人",
            )
            self.db.session.add(app)
        return app

    def get_app(self, id: uuid.UUID) -> App:
        """
        获取 AI 应用
        """
        # 查询数据库获取应用实例
        app = self.db.session.query(App).filter_by(id=id).first()
        # 返回应用实例
        return app

    def update_app(self, id: uuid.UUID) -> App:
        """
        更新 AI 应用
        """
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "更新后的聊天机器人"
        return app

    def delete_app(self, id: uuid.UUID) -> App:
        """
        删除 AI 应用
        """
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        return app