#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : chyu-wissfi
@Email : chyu.wissfi@gmail.com
@File   : chat.py
"""
import os
from typing import Tuple

import tiktoken
from langchain_openai.chat_models.base import BaseChatOpenAI

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Chat(BaseChatOpenAI, BaseLanguageModel):
    """月之暗面聊天模型"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            openai_api_key=os.getenv("MOONSHOT_API_KEY"),
            openai_api_base="https://api.moonshot.cn/v1",
            **kwargs
        )

    def _get_encoding_model(self) -> Tuple[str, tiktoken.Encoding]:
        """重写月之暗面获取编码模型名字+模型函数，该类继承OpenAI，词表模型可以使用gpt-3.5-turbo防止出错"""
        # 1.将DeepSeek的词表模型设置为gpt-3.5-turbo
        model = "gpt-3.5-turbo"

        # 2.返回模型名字+编码器
        return model, tiktoken.encoding_for_model(model)
