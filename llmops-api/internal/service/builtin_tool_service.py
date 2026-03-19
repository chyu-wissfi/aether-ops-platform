"""
@Time: 2026/03/19
@Author: chyu.wissfi@gmail.com
@Description: Builtin tool service
"""
from dataclasses import dataclass
from injector import inject
from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
from internal.core.tools.builtin_tools.categories import BuiltinCategoryManager
from internal.exception import NotFoundException
from pydantic import BaseModel, Field
from flask import current_app
import os
import mimetypes
from typing import Any

@inject
@dataclass
class BuiltinToolService:
    """
    内置工具服务
    """
    builtin_provider_manager: BuiltinProviderManager
    builtin_category_manager: BuiltinCategoryManager


    def get_builtin_tools(self) -> list:
        """
        获取LLMOps所有内置工具+提供商对应的信息
        """
        # 1. 获取所有服务提供商
        providers = self.builtin_provider_manager.get_providers()
       
        # 2. 遍历所有服务提供商并提取工具信息
        builtin_tools = []
        for provider in providers:
            provider_entity = provider.provider_entity
            builtin_tool = {
                **provider_entity.model_dump(exclude=["icon"]),
                "tools": [],
            }
            # 3. 遍历并提取提供商的所有工具实体
            for tool_entity in provider.get_tool_entities():
                # 4. 获取工具函数
                tool = provider.get_tool(tool_entity.name)
                # 5. 构建工具实体信息
                tool_dic = {
                    **tool_entity.model_dump(),
                    "inputs": self.get_tool_input(tool),
                }
                builtin_tool["tools"].append(tool_dic)

            builtin_tools.append(builtin_tool)

        return builtin_tools
        

    def get_provider_tool(self, provider_name: str, tool_name: str) -> dict:
        """
        根据服务提供商名字和工具名字获取指定工具信息
        """
        # 1. 获取内置的服务提供商
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"该服务提供商不存在: {provider_name}")
        
        # 2. 获取该服务提供商下的指定工具
        tool_entity = provider.get_tool_entity(tool_name)
        if tool_entity is None:
            raise NotFoundException(f"该服务提供商下不存在该工具: {tool_name}")

        # 3. 组装提供商和工具实体信息
        provider_entity = provider.provider_entity
        tool = provider.get_tool(tool_name)

        builtin_tool = {
            "provider": {**provider_entity.model_dump(exclude=["icon", "created_at"])},
            **tool_entity.model_dump(),
            "created_at": provider_entity.created_at,
            "inputs": self.get_tool_input(tool),
        }

        return builtin_tool


    def get_provider_icon(self, provider_name: str) -> tuple[bytes, str]:
        """
        根据服务提供商名字获取指定服务提供商的图标流信息
        """
        # 1. 获取内置的服务提供商
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"该服务提供商不存在: {provider_name}")
        
        # 2. 获取项目的根路径并拼接图标路径
        root_path = os.path.dirname(os.path.dirname(current_app.root_path))
        provider_path = os.path.join(
            root_path, 
            "internal", "core", "tools", "builtin_tools", "providers", provider_name,
        )
        icon_path = os.path.join(provider_path, "_asset", provider.provider_entity.icon)

        # 3. 检测icon是否存在
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"该服务提供商_asset下的图标不存在: {icon_path}")

        # 4. 获取图标MIME类型
        mimetype, _ = mimetypes.guess_type(icon_path)
        mimetype = mimetype or "application/octet-stream"

        # 5. 读取图标流
        with open(icon_path, "rb") as f:
            byte_data = f.read()
            return byte_data, mimetype


    def get_categories(self) -> list[str, Any]:
        """
        获取所有内置提供商的工具分类信息，涵盖了category、name、icon
        """
        category_map = self.builtin_category_manager.get_category_map()
        return [{
            "name": category["entity"].name,
            "category": category["entity"].category,
            "icon": category["icon"],
        } for category in category_map.values()]


    @classmethod
    def get_tool_input(cls, tool) -> list:
        """
        根据传入的工具函数，获取指定工具的输入参数信息
        """
        inputs = []
        if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):
            for field_name, model_field in tool.args_schema.model_fields.items():
                inputs.append({
                    "name": field_name,
                    "description": model_field.description or "",
                    "type": model_field.annotation.__name__ if hasattr(model_field.annotation, "__name__") else str(model_field.annotation),
                    "required": model_field.is_required(),
                })

        return inputs

    