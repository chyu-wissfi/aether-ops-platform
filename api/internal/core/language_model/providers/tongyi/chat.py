#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : chyu-wissfi
@Email : chyu.wissfi@gmail.com
@File   : chat.py
"""
from langchain_community.chat_models.tongyi import ChatTongyi

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Chat(ChatTongyi, BaseLanguageModel):
    """通义千问聊天模型"""
    pass
