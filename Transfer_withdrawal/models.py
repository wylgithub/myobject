#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from user_account.models import User


class Transfer(models.Model):
    """
    家庭流水管理之--转账
    """
    create_datetime = models.DateTimeField(auto_now_add=True)  # 添加时间
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    transfer_amount = models.DecimalField(u'转出金额', max_digits=8, decimal_places=2, default=0)  # 转账金额
    remarks = models.TextField(u"备注", null=True, blank=True)  # 备注的添加用于描述这笔收入的具体来源和数量描述
    handler = models.CharField(u"转出人", max_length=255, null=True, blank=True)  # 处理者:添加信息的人
    borrow_person = models.CharField(u"接受转款人", max_length=255, null=True, blank=True)  # 金额转出的接受对象
    transfer_accounts = models.ImageField(u"转出账户", max_length=10, null=True, blank=True)  # 款项转出账户
    into_accounts = models.ImageField(u"转入账户", max_length=10, null=True, blank=True)  # 款项转出账户
    out_bank = models.CharField(u'转出银行', max_length=20)
    into_bank = models.CharField(u'转入银行', max_length=20)
    user = models.ForeignKey(User, verbose_name=u"家庭支出管理信息登记人", blank=True, null=True, related_name='user_transfer')

    class Meta:
        db_table = 'graduation_design_transfer'


class Withdrawal(models.Model):
    """
    家庭流水管理之--取款
    """
    create_datetime = models.DateTimeField(auto_now_add=True)  # 添加时间
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    w_amount = models.DecimalField(u'取款金额', max_digits=8, decimal_places=2, default=0)  #收入金额
    remarks = models.TextField(u"备注", null=True, blank=True)  # 备注的添加用于描述这笔收入的具体来源和数量描述
    handler = models.CharField(u"取款者", max_length=255, null=True, blank=True)  # 处理者:添加信息的人
    out_bank = models.CharField(u'取款银行', max_length=20) # 取款银行
    transfer_accounts = models.IntegerField(u"取款账户", max_length=255, null=True, blank=True)  # 款项取出账户,
    balance = models.CharField(u"账户余额", max_length=255, null=True, blank=True)  # 款项取出后账户余额,
    user = models.ForeignKey(User, verbose_name=u"家庭取款管理信息登记人", blank=True, null=True, related_name='user_width')

    class Meta:
        db_table = 'graduation_design_withdrawals'