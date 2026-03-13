"""
@Time: 2026/3/5
@Author: chyu.wissfi@gmail.com
@Description: HTTP server module
"""
from re import A, M
from flask import Flask
from flask_cors import CORS
from internal.router import Router
from config import Config
from internal.exception import CustomException
from pkg.response import json, Response, HttpCode
import os
from pkg.sqlalchemy import SQLAlchemy
from internal.model.app import App
from flask_migrate import Migrate


class Http(Flask):
    """
    HTTP 服务引擎
    """
    def __init__(
            self, 
            *args,
            conf: Config,
            db: SQLAlchemy,
            migrate: Migrate,
            router: Router,
            **kwargs
        ) -> None:
        super().__init__(*args, **kwargs) 
        # 1. 初始化应用配置
        self.config.from_object(conf)
    
        # 2.注册绑定异常处理
        self.register_error_handler(Exception, self._register_error_handler)

        # 3.初始化Flask扩展
        db.init_app(self)
        migrate.init_app(self, db, directory="internal/migration")
        
        # 4. 解决前后端跨越问题
        CORS(self, resources={
            r"/*": {
                "origins": "*",
                "supports_credentials": True,
                # "methods": ["GET", "POST"],
                # "allowed_headers": ["Content-Type"],
            }
        })

        # 5. 注册应用路由
        router.register_router(self)

    def _register_error_handler(self, error: Exception):
        """
        注册异常处理函数
        """
        # 1. 异常信息是不是我们自定义的异常，如果是可以提取message和code等信息
        if isinstance(error, CustomException):
            return json(Response(
                code = error.code,
                message = error.message,
                data = error.data if error.data is not None else {}
            ))
        
        # 2. 处理 HTTP 异常（如 404, 405 等）
        from werkzeug.exceptions import HTTPException
        if isinstance(error, HTTPException):
            return json(Response(
                code=error.code,
                message=error.description,
                data={}
            ), status_code=error.code)
        
        # 3. 如果不是我们自定义的异常，则有可能是程序或数据库抛出的异常，也可以提取信息，设置为FAIL状态码
        if self.debug or os.getenv("Flask_ENV") == "development": 
            raise error
        else:
            return json(Response(code=HttpCode.FAIL, message=str(error), data={}))
