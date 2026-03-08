"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: 扩展模块的依赖注入
"""
from injector import Module, Binder
from pkg.sqlalchemy import SQLAlchemy
from internal.extension.database_extension import db

class ExtensionModule(Module):
    """
    扩展模块的依赖注入
    """
    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)

