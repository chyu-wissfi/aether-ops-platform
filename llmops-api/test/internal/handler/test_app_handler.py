"""
@Time: 2026/3/6
@Author: chyu.wissfi@gmail.com
@Description: Test app handler
"""
from pkg.response import HttpCode
import pytest

class TestAppHandler:
    """
    app控制器的测试类
    """
    @pytest.mark.parametrize(
        "app_id, query",
        [
            ("8d62b2ef-391b-46d0-b851-e3e4165402e7", None),
            ("8d62b2ef-391b-46d0-b851-e3e4165402e7", "你好，你是？")
        ]   
    )
    def test_completion(self, app_id, query, client):
        """
        测试聊天接口
        """
        resp = client.post(f"/apps/{app_id}/debug", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
