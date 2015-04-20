#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from user_account.models import User


class Pay(models.Model):
    """
    家庭收入管理模型
    """
    pay_type = models.CharField(u"家庭支出类型", max_length=10)  # 家庭收入类型字段,也就是收入来源
    create_datetime = models.DateTimeField(auto_now_add=True)  # 添加时间
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    pay_amount = models.DecimalField(u'收入金额', max_digits=8, decimal_places=2, default=0)  #收入金额
    remarks = models.TextField(u"备注", null=True, blank=True)  # 备注的添加用于描述这笔收入的具体来源和数量描述
    handler = models.CharField(u"处理者", max_length=255, null=True, blank=True)  # 处理者:添加信息的人
    user = models.ForeignKey(User, verbose_name=u"家庭支出管理信息登记人", blank=True, null=True, related_name='user_pay')

    class Meta:
        db_table = 'graduation_design_pay'