#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


from utility.constant import INCOME_TYPE_FOR_WORK, INCOME_TYPE_CHOICE


class Income(models.Model):
    """
    家庭收入管理模型
    """
    income_type = models.PositiveSmallIntegerField(u"家庭收入类型", max_length=10, choices=INCOME_TYPE_CHOICE,
                                                   default=INCOME_TYPE_FOR_WORK)  # 家庭收入类型字段,也就是收入来源
    create_datetime = models.DateTimeField(auto_now_add=True)  # 添加时间
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    income_amount = models.DecimalField(u'收入金额', max_digits=8, decimal_places=2, default=0)  #收入金额
    remarks = models.TextField(u"备注", null=True, blank=True)  # 备注的添加用于描述这笔收入的具体来源和数量描述
    handler = models.CharField(u"处理者", max_length=255, null=True, blank=True)  # 处理者:添加信息的人

    class Meta:
        db_table = 'graduation_design_income'
