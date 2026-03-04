"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: HTTP server application
"""
from injector import Injector
from internal.server import Http
from internal.router import Router

# 初始化依赖注入容器
injector = Injector()

app = Http(__name__, router=injector.get(Router))


if __name__ == "__main__":
    app.run(debug=True)
