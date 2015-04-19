#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.db import models

from django.forms import ModelForm, Form
from utility.constant import INCOME_TYPE_FOR_WORK, INCOME_TYPE_CHOICE


class Income(models.Model):
    """
    家庭收入管理模型
    """
    income_type = models.CharField(u"家庭收入类型", max_length=10)  # 家庭收入类型字段,也就是收入来源
    create_datetime = models.DateTimeField(auto_now_add=True)  # 添加时间
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    income_amount = models.DecimalField(u'收入金额', max_digits=8, decimal_places=2, default=0)  #收入金额
    remarks = models.TextField(u"备注", null=True, blank=True)  # 备注的添加用于描述这笔收入的具体来源和数量描述
    handler = models.CharField(u"处理者", max_length=255, null=True, blank=True)  # 处理者:添加信息的人

    class Meta:
        db_table = 'graduation_design_income'


# 添加收入表单提交Form表单
class IncomeForm(Form):
    """
    收入Form
    """
    recode_name = forms.CharField(required=False)  # 记录人姓名
    income_type = forms.CharField(required=False)  # 收入类型
    income_amount = forms.IntegerField(required=False)  # 收入数量
    recode_date = forms.DateTimeField(required=False)  # 记录日期
    remark = forms.Textarea()  # 备注

    def clean(self):
        cleaned_data = super(IncomeForm, self).clean()

        # 添加记录人的姓名
        if 'recode_name' in cleaned_data:
            name = cleaned_data['recode_name']
            if name is u'':
                msg = u"记录人的姓名不可以为空!"
                self._errors['recode_name'] = self.errror_class([msg])

        # 判断收入类型是否满足要求
        if 'income_type' in cleaned_data:
            itype = cleaned_data['income_type']
            if itype is u'':
                msg = u'收入类型不可以为空!'
                self._errors['income_type'] = self.error_class([msg])

        # 判断收入金额是满足要求
        if 'income_amount' in cleaned_data:
            amount = cleaned_data['income_amount']
            int_amount = int(amount)
            if int_amount is u'' or int_amount <= 0:
                msg = u"收入金额不允许为空,并且必须大于0!"
                self._errors['income_amount'] = self.error_class([msg])

        # 日期是否合适:
        if 'recode_date' in cleaned_data:
            r_date = cleaned_data['recode_date']

            if r_date is u'':
                msg = u'请填写记录撰写时间!'
                self._errors['recode_date'] = self.error_class([msg])

        # 判断是否有备注
        if 'remark' in cleaned_data:
            remarks = cleaned_data['remark']

            if remarks is u'':
                msg = u'请输入本次收入的具体来源,以防以后对账!'
                self._errors['remark'] = self.error_class([msg])

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)

