#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

from user_account.models import User


class Lend(models.Model):
    """
    家庭流水管理之--借出
    """
    user = models.ForeignKey(User, verbose_name=u"家庭借出管理信息登记人", blank=True, null=True, related_name='user_lend')
    lend_amount = models.DecimalField(u'借出金额', max_digits=8, decimal_places=2, default=0)  # 借出金额
    back_amount = models.DecimalField(u'已还金额', max_digits=8, decimal_places=2, default=0)  # 已经还了的金额
    own_amount = models.DecimalField(u'还欠金额', max_digits=8, decimal_places=2, default=0)  # 现在还欠的金额
    borrow_person = models.CharField(u"借出人", max_length=255, null=True, blank=True)  # 借出款项人
    lend_person = models.CharField(u"借入人", max_length=255, null=True, blank=True)  # 借入款项人
    handler = models.CharField(u"借款信息记录人", max_length=255, null=True, blank=True)  # 金额转出的接受对象
    lend_type = models.ImageField(u"借出类型", max_length=10, null=True, blank=True)  # 借款方式(可以是转账或者现金等方式)
    into_accounts = models.ImageField(u"借出账户", max_length=10, null=True, blank=True)  # 款项借出账户
    pay_accounts = models.ImageField(u"还款账户", max_length=10, null=True, blank=True)  # 还款账户有时要求款项打到别人的账户,因此这里有一个还款账户比较妥当
    into_bank = models.CharField(u'借出银行', max_length=20)
    pay_bank = models.CharField(u'还款银行', max_length=20)
    lend_datetime = models.DateTimeField(auto_now_add=True)  # 借出日期
    pay_datetime = models.DateTimeField(auto_now_add=True)  # 预计还款日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    remarks = models.TextField(u"备注", null=True, blank=True)  # 备注的添加用于描述这笔借款的具体来源和数量描述

    class Meta:
        db_table = 'graduation_design_lend'