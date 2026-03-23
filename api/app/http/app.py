#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : chyu-wissfi
@Email : chyu.wissfi@gmail.com
@File   : app.py
"""
from langchain_core.utils import _merge

from internal.core.langchain_fix.langchain_core_utils__merge import merge_lists

# 1.langchain补丁包
_merge.merge_lists = merge_lists

import dotenv
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_weaviate import FlaskWeaviate

from config import Config
from internal.middleware import Middleware
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy
from .module import injector

# 2.将env加载到环境变量中
dotenv.load_dotenv()

# 3.构建LLMOps项目配置
conf = Config()

app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    weaviate=injector.get(FlaskWeaviate),
    migrate=injector.get(Migrate),
    login_manager=injector.get(LoginManager),
    middleware=injector.get(Middleware),
    router=injector.get(Router),
)

celery = app.extensions["celery"]

if __name__ == "__main__":
    app.run(debug=True)
