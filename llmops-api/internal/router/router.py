"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: router.py
"""
from dataclasses import dataclass
from flask import Flask, Blueprint
from internal.handler import AppHandler, BuiltinToolHandler
from injector import inject


@inject
@dataclass
class Router:
    """
    Router class
    """
    app_handler: AppHandler
    builtin_tool_handler: BuiltinToolHandler


    def register_router(self, app: Flask):
        """
        Register router
        """
        # 1.创建一个蓝图
        bp = Blueprint("llmops", __name__,url_prefix="") 
        
        # 2.将url与对应的控制器做绑定
        bp.add_url_rule("/ping", view_func=self.app_handler.ping)
        bp.add_url_rule("/apps/<uuid:app_id>/debug", methods=["POST"], view_func=self.app_handler.debug)
        bp.add_url_rule("/app", methods=["POST"], view_func=self.app_handler.create_app)
        bp.add_url_rule("/app/<uuid:id>", view_func=self.app_handler.get_app)  # 默认GET方法
        bp.add_url_rule("/app/<uuid:id>/update", methods=["POST"], view_func=self.app_handler.update_app)
        bp.add_url_rule("/app/<uuid:id>/delete", methods=["POST"], view_func=self.app_handler.delete_app)
        
        # 3. 内置插件广场模块
        bp.add_url_rule("/builtin-tools", view_func=self.builtin_tool_handler.get_builtin_tools)
        bp.add_url_rule("/builtin-tools/<string:provider_name>/tools/<string:tool_name>", view_func=self.builtin_tool_handler.get_provider_tool)
        bp.add_url_rule("/builtin-tools/<string:provider_name>/icon", view_func=self.builtin_tool_handler.get_provider_icon)
        bp.add_url_rule("/builtin-tools/categories", view_func=self.builtin_tool_handler.get_categories)
        
        # 4. 将蓝图注册到app中
        app.register_blueprint(bp)

