#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


from utility.constant import INCOME_TYPE_DICT, INCOME_TYPE_FOR_WORK


class Income(models.Model):
    """
    家庭收入管理模型
    """
    income_type = models.CharField(u'家庭收入类型', max_length=10, choices=INCOME_TYPE_DICT, default=INCOME_TYPE_FOR_WORK)  # 家庭收入类型字段
    create_datetime = models.DateTimeField(auto_now_add=True)  # 添加时间
    income_amount = models.DecimalField(u'收入金额', decimal_places=2, default=0)