#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : chyu-wissfi
@Email : chyu.wissfi@gmail.com
@File   : chat.py
"""
from langchain_ollama import ChatOllama

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Chat(ChatOllama, BaseLanguageModel):
    """Ollama聊天模型"""
    base_url = "http://60.247.21.102:9432"
