#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.db import models

# Create your models here.
from django.forms import ModelForm
from user_account.models import User


class Weekly(models.Model):
    """
    周流水计划model
    """
    user = models.ForeignKey(User, verbose_name=u"添加家庭支出管理信息", blank=True, null=True, related_name='user_weekly_plan')
    start_date = models.DateTimeField(u"开始日期")  # 周流水计划开始日期
    end_date = models.DateTimeField(u"结束日期")    # 周流水计划结束日期
    update_datetime = models.DateTimeField(u'更新时间', auto_now=True)  # 支出信息更新日期
    work_income = models.PositiveIntegerField(u"周预计工作收入", max_length=20, default=0)   # 每个礼拜预计工作收入
    investment_income = models.PositiveIntegerField(u"周预计投资收入", max_length=20, default=0)   # 每个礼拜预计个人投资理财收入
    life_spend = models.PositiveIntegerField(u"生活支出", max_length=20, default=0)    # 每个礼拜预计的生活
    other_spend = models.PositiveIntegerField(u"其它支出", max_length=20, default=0)    # 每个礼拜预计的其它
    remarks = models.TextField(u"备注信息") # 添加备注
    handler = models.CharField(u"处理者", max_length=255)  # 处理者:添加信息的人
    delete_flg = models.BooleanField(u"删除标识为", default=False)   # 字段删除标志为

    class Meta:
        db_table = "weekly_plan"


class Monthly(models.Model):
    """
    月流水model
    """
    user = models.ForeignKey(User, verbose_name=u"添加家庭支出管理信息", blank=True, null=True, related_name='user_monthly_plan')
    start_date = models.DateTimeField(u"开始日期")  # 周流水计划开始日期
    end_date = models.DateTimeField(u"结束日期")    # 周流水计划结束日期
    update_datetime = models.DateTimeField(u'更新时间', auto_now=True)  # 支出信息更新日期
    work_income = models.PositiveIntegerField(u"周预计工作收入", max_length=20, default=0)   # 每个月预计工作收入
    investment_income = models.PositiveIntegerField(u"周预计投资收入", max_length=20, default=0)   # 每个月预计个人投资理财收入
    life_spend = models.PositiveIntegerField(u"生活支出", max_length=20, default=0)    # 每个月预计的生活
    other_spend = models.PositiveIntegerField(u"其它支出", max_length=20, default=0)    # 每个月预计的其它
    remarks = models.TextField(u"备注信息") # 添加备注
    handler = models.CharField(u"处理者", max_length=255)  # 处理者:添加信息的人
    delete_flg = models.BooleanField(u"删除标识为", default=False)   # 字段删除标志为

    class Meta:
        db_table = "monthly_plan"


# 添加月流水计划表单提交Form表单
class MonthlyForm(ModelForm):
    """
    收入Form
    """
    def clean(self):
        cleaned_data = super(MonthlyForm, self).clean()

        # # 日期是否合适:
        if 'start_date' and 'end_date' in cleaned_data:
            # 获取前端起始和截止日期
            r_date = cleaned_data['start_date'].date()
            e_date = cleaned_data['end_date'].date()

            # 起始日期和截止日期相减
            sub_day = (e_date - r_date).days

            if sub_day < 28 or sub_day > 32 or sub_day is None:
                msg = u"选择的日期不满足一个月的需求!"
                self._errors['end_date'] = self.error_class([msg])

                del cleaned_data['end_date']

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(MonthlyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Monthly
        fields = ('start_date', 'end_date', 'work_income', 'handler', 'investment_income',
                  'life_spend', 'other_spend', 'remarks')


class Yearly(models.Model):
    """
    年流水计划model
    """
    user = models.ForeignKey(User, verbose_name=u"添加年流水计划操作人外检", blank=True, null=True,
                             related_name='user_yearly_plan')
    # 添加年流水计划操作人
    start_date = models.DateTimeField(u"开始日期")  # 年流水计划开始日期
    end_date = models.DateTimeField(u"结束日期")    # 年流水计划结束日期
    update_datetime = models.DateTimeField(u'更新时间', auto_now=True)  # 支出信息更新日期
    work_income = models.PositiveIntegerField(u"周预计工作收入", max_length=20, default=0)   # 每年预计工作收入
    investment_income = models.PositiveIntegerField(u"周预计投资收入", max_length=20, default=0)   # 每年预计个人投资理财收入
    life_spend = models.PositiveIntegerField(u"生活支出", max_length=20, default=0)    # 每年预计的生活
    other_spend = models.PositiveIntegerField(u"其它支出", max_length=20, default=0)    # 每年月预计的其它
    remarks = models.TextField(u"备注信息") # 添加备注
    handler = models.CharField(u"处理者", max_length=255)  # 处理者:添加信息的人
    delete_flg = models.BooleanField(u"删除标识为", default=False)   # 字段删除标志为

    class Meta:
        db_table = "yearly_plan"


# 添加月流水计划表单提交Form表单
class YearlyForm(ModelForm):
    """
    收入Form
    """
    def clean(self):
        cleaned_data = super(YearlyForm, self).clean()

        # # 日期是否合适:
        if 'start_date' and 'end_date' in cleaned_data:
            # 获取前端起始和截止日期
            r_date = cleaned_data['start_date'].date()
            e_date = cleaned_data['end_date'].date()

            # 起始日期和截止日期相减
            sub_day = (e_date - r_date).days

            sub_day_to_int = int(sub_day)

            if sub_day < 365 or sub_day > 366 or sub_day is None:
                msg = u"选择的日期不满足一个月的需求!"
                self._errors['end_date'] = self.error_class([msg])

                del cleaned_data['end_date']

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(YearlyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Yearly
        fields = ('start_date', 'end_date', 'work_income', 'handler', 'investment_income',
                  'life_spend', 'other_spend', 'remarks')