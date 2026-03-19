"""
@Time: 2026/03/19
@Author: chyu.wissfi@gmail.com
@Description: Builtin tool handler
"""

from injector import inject
from internal.service.builtin_tool_service import BuiltinToolService
from dataclasses import dataclass
from pkg.response import success_json
from flask import send_file
import io

@inject
@dataclass
class BuiltinToolHandler:
    """
    内置工具处理器
    """
    builtin_tool_service: BuiltinToolService

    def get_builtin_tools(self) -> list:
        """
        获取LLMOps所有内置工具信息+提供商信息
        """
        builtin_tools = self.builtin_tool_service.get_builtin_tools()    
        return success_json(builtin_tools)
        
    def get_provider_tool(self, provider_name: str, tool_name: str = None) -> dict:
        """
        根据提供商名称和工具名称获取工具信息
        """
        builtin_tool = self.builtin_tool_service.get_provider_tool(provider_name, tool_name)
        return success_json(builtin_tool)

    def get_provider_icon(self, provider_name: str):
        """
        根据提供商名称获取提供商图标流信息
        """
        icon, mimetype = self.builtin_tool_service.get_provider_icon(provider_name)
        return send_file(io.BytesIO(icon), mimetype)



    def get_categories(self):
        """
        获取所有内置提供商的工具分类信息
        """
        categories = self.builtin_tool_service.get_categories()
        return success_json(categories)
