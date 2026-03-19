"""
@Time: 2026/3/19
@Author: chyu.wissfi@gmail.com
@Description: Test builtin tool handler
"""
from pkg.response import HttpCode
import pytest


class TestBuiltinToolHandler:
    """
    builtin tool控制器的测试类
    """
    
    def test_get_categories(self, client):
        """
        测试获取所有内置工具分类信息
        """
        resp = client.get("/builtin-tools/categories")
        assert resp.status_code == 200
        assert resp.json.get("code") == HttpCode.SUCCESS
        assert len(resp.json.get("data")) > 0
       
    def test_get_builtin_tools(self, client):
        """
        测试获取所有内置工具
        """
        resp = client.get("/builtin-tools")
        assert resp.status_code == 200
        assert resp.json.get("code") == HttpCode.SUCCESS
        assert len(resp.json.get("data")) > 0

    @pytest.mark.parametrize(
        "provider_name, tool_name",
        [
            ("google", "google_serper"),
            ("wissfi", "llmops"),
        ]
    )
    def test_get_provider_tools(self, provider_name, tool_name, client):
        """
        测试获取指定工具接口
        """
        resp = client.get(f"/builtin-tools/{provider_name}/tools/{tool_name}")
        assert resp.status_code == 200
        if provider_name == "google":
            assert resp.json.get("code") == HttpCode.SUCCESS
            assert resp.json.get("data").get("name") == tool_name
        elif provider_name == "wissfi":
            assert resp.json.get("code") == HttpCode.NOT_FOUND

    @pytest.mark.parametrize("provider_name", ["google", "wissfi"])
    def test_get_provider_icon(self, provider_name, client):
        """
        测试获取指定提供商的icon接口
        """
        resp = client.get(f"/builtin-tools/{provider_name}/icon")
        assert resp.status_code == 200
        if provider_name == "wissfi":
            assert resp.json.get("code") == HttpCode.NOT_FOUND
