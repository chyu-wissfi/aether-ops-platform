#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author : chyu-wissfi
@Email : chyu.wissfi@gmail.com
@File   : platform_entity.py
"""
from enum import Enum


class WechatConfigStatus(str, Enum):
    """微信配置状态"""
    CONFIGURED = "configured"  # 已配置
    UNCONFIGURED = "unconfigured"  # 未配置
