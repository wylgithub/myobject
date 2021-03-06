#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.db import models
import datetime

from django.forms import ModelForm
from user_account.models import User


class Income(models.Model):
    """
    家庭收入管理模型
    """
    user = models.ForeignKey(User, verbose_name=u"家庭收入管理信息登记人", blank=True, null=True, related_name='user_income')
    income_type = models.CharField(u"家庭收入类型", max_length=10)  # 家庭收入类型字段,也就是收入来源
    create_datetime = models.DateTimeField()  # 添加时间
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    income_amount = models.DecimalField(u'收入金额', max_digits=8, decimal_places=2, default=0)  #收入金额
    remarks = models.TextField(u"备注")  # 备注的添加用于描述这笔收入的具体来源和数量描述
    handler = models.CharField(u"处理者", max_length=255)  # 处理者:添加信息的人
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = 'graduation_design_income'


# 添加收入表单提交Form表单
class IncomeForm(ModelForm):
    """
    收入Form
    """
    recode_date = forms.DateTimeField(required=False)  # 记录日期

    def clean(self):
        cleaned_data = super(IncomeForm, self).clean()

        # 添加记录人的姓名
        if 'handler' in cleaned_data:
            name = cleaned_data['handler']
            if name is u'':
                msg = u"记录人的姓名不可以为空!"
                self._errors['handler'] = self.errror_class([msg])

                del cleaned_data['handler']

        # 判断收入类型是否满足要求
        if 'income_type' in cleaned_data:
            itype = cleaned_data['income_type']
            if itype is u'' or itype.isdigit():
                msg = u'收入类型不可以为空和全为数字!!'
                self._errors['income_type'] = self.error_class([msg])

                del cleaned_data['income_type']

        # 判断收入金额是满足要求
        if 'income_amount' in cleaned_data:
            amount = cleaned_data['income_amount']

            if amount is u'' or amount <= 0:
                msg = u"收入金额不允许为空,并且必须大于0!"
                self._errors['income_amount'] = self.error_class([msg])

                del cleaned_data['income_amount']

        # 日期是否合适:
        # if 'create_datetime' in cleaned_data:
        #     r_date = cleaned_data['create_datetime']
        #     # 获取当前时间date类型
        #     today = datetime.date.today()
        #
        #     # 将前端传过来的datetime转换为date
        #     todate = r_date.date()
        #     if r_date is u'' or todate > today:
        #         msg = u'请填写记录撰写时间(时间必须小于等于当前日期)!'
        #         self._errors['create_datetime'] = self.error_class([msg])
        #
        #         del cleaned_data['create_datetime']

        # 判断是否有备注:这个备注可有可无,因为不是每一笔收入有要写入备注,
        # if 'remark' in cleaned_data:
        #     remarks = cleaned_data['remark']
        #
        #     if remarks is u'':
        #         msg = u'请输入本次收入的具体来源,以防以后对账!'
        #         self._errors['remark'] = self.error_class([msg])
        #
        #     del cleaned_data['remark']

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Income
        fields = ('income_type', 'income_amount', 'remarks', 'handler', 'create_datetime')


class IncomeEditForm(ModelForm):
    update_datetime = models.DateTimeField()  # 更新时间

    class Meta:
        model = Income
        fields = ('income_type', 'income_amount', 'remarks', 'handler')


class Expend(models.Model):
    """
    家庭支出管理模型
    """
    user = models.ForeignKey(User, verbose_name=u"添加家庭支出管理信息", blank=True, null=True, related_name='user_expend')
    expend_type = models.CharField(u"家庭支出类型", max_length=50)  # 家庭支出类型字段,也就是支出去向
    expend_account = models.CharField(u"家庭支出交易账户", max_length=50)  # 家庭支出交易账户
    expend_amount = models.DecimalField(u'支出金额', max_digits=8, decimal_places=2, default=0)  #支出金额
    balance = models.DecimalField(u'账户余额', max_digits=10, decimal_places=2, default=0)  #账户余额
    create_datetime = models.DateTimeField(u'录入时间')  # 添加支出信息时间
    update_datetime = models.DateTimeField(u'更新时间', auto_now=True)  # 支出信息更新日期
    remarks = models.TextField(u"备注", max_length=500)  # 备注的添加用于描述这笔收入的具体来源和数量描述
    handler = models.CharField(u"添加支出信息的处理者", max_length=255)  # 处理者:添加支出信息的人
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = 'graduation_design_expend'


class ExpendForm(ModelForm):
    """
    家庭支出信息表单提交Form
    """
    def clean(self):
        cleaned_data = super(ExpendForm, self).clean()

        # 家庭支出信息后端check开始
        if 'expend_type' in cleaned_data:
            expend_type = cleaned_data['expend_type']
            if expend_type in u'' or (expend_type.isdigit()):
                msg = u"请输入正确的支出类型(不可以全为数字!)"
                self._errors['expend_type'] = self.error_class([msg])

                del cleaned_data['expend_type']

        if 'expend_amount' in cleaned_data:
            expend_data = cleaned_data['expend_amount']

            if expend_data is u'':
                msg = u'支出金额不可以为空,且必须为数字!'
                self._errors['expend_amount'] = self.error_class([msg])

                del cleaned_data['expend_amount']

        if 'expend_account' in cleaned_data:
            expend_data = cleaned_data['expend_account']

            expend_length = str(expend_data).__len__()

            if expend_data is u'' or (not expend_data.isdigit()):
                msg = u'支出账户不可以为空,且必须为数字!'
                self._errors['expend_account'] = self.error_class([msg])

                del cleaned_data['expend_account']

            if expend_length != 19:
                msg = u'支出账户为银行账户,应该为19位合法数字组成,例如:622848 003816516 2378'
                self._errors['expend_account'] = self.error_class([msg])

                del cleaned_data['expend_account']

        # if 'create_datetime' in cleaned_data:
        #     create_datetime = cleaned_data['create_datetime']
        #
        #     c_date = create_datetime.date()
        #     n_date = datetime.date.today()
        #     if create_datetime is u"" or c_date > n_date:
        #         msg = u"请填写正确的支出时间(支出时间必须小于当前时间!)!"
        #
        #         self._errors['create_datetime'] = self.error_class([msg])
        #
        #         del cleaned_data['create_datetime']
        # 家庭支出信息后端check结束
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ExpendForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Expend
        fields = ('expend_type', 'expend_account', 'expend_amount', 'balance', 'remarks', 'handler', 'create_datetime')


class Borrow(models.Model):
    """
    家庭流水管理之--借入
    """
    user = models.ForeignKey(User, verbose_name=u"家庭借入管理信息登记人", blank=True, null=True, related_name='user_borrow')
    borrow_amount = models.DecimalField(u'借入金额', max_digits=8, decimal_places=2, default=0)  # 借入金额
    balance = models.DecimalField(u'账户余额', max_digits=8, decimal_places=2, default=0)  # 账户余额
    borrow_person = models.CharField(u"借入人", max_length=255)  # 借入款项人
    lend_person = models.CharField(u"借出人", max_length=255)  # 借出款项人
    handler = models.CharField(u"借款信息记录人", max_length=255)  # 登记信息人员
    borrow_datetime = models.DateTimeField()  # 借入日期
    repay_datetime = models.DateTimeField()  # 预计还款日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    remarks = models.TextField(u"备注", null=True, blank=True)  # 备注的添加用于描述这笔借款的具体来源和数量描述
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = 'graduation_design_borrow'


class BorrowForm(ModelForm):
    """
    家庭借入信息表单提交Form
    """
    def clean(self):
        cleaned_data = super(BorrowForm, self).clean()
        # 家庭借入信息后端check开始
        if 'borrow_person' in cleaned_data:
            borrow_person = cleaned_data['borrow_person']
            if borrow_person is u"":
                msg = u"借款人不可以为空,默认为当前登录用户!"
                self._errors['borrow_person'] = self.error_class([msg])

                del cleaned_data['borrow_person']

        if 'lend_person' in cleaned_data:
            lend_person = cleaned_data['lend_person']
            if lend_person is u"" or lend_person.isdigit():
                msg = u"借出款人不可以为空,且必须为有效的名字!!"
                self._errors['lend_person'] = self.error_class([msg])

                del cleaned_data['lend_person']

        if 'borrow_amount' in cleaned_data:
            borrow_amount = cleaned_data['borrow_amount']
            amount = float(borrow_amount)
            if borrow_amount is u"" or amount <= 0:
                msg = u"请填入有效的借入金额(例如:100,单位默认为元)!!"
                self._errors['borrow_amount'] = self.error_class([msg])

                del cleaned_data['borrow_amount']

        if 'balance' in cleaned_data:
            balance = cleaned_data['balance']
            amount = float(balance)
            if balance is u"" or amount < 0:
                msg = u"余额再怎么少,也不可能小雨0吧!"
                self._errors['balance'] = self.error_class([msg])

                del cleaned_data['balance']

        # if 'borrow_datetime' in cleaned_data:
        #     borrow_datetime = cleaned_data['borrow_datetime']
        #     # 前端传过来的时间,将其格式化为日期格式
        #     b_date = borrow_datetime.date()
        #
        #     # 获取当前日期
        #     n_date = datetime.date.today()
        #
        #     if borrow_datetime is u"" or b_date > n_date:
        #         msg = u"请选择有效的借入时间(借入时间不可以大于当前时间)!!"
        #         self._errors['borrow_datetime'] = self.error_class([msg])
        #
        #         del cleaned_data['borrow_datetime']

        # if 'repay_datetime' in cleaned_data:
        #     repay_datetime = cleaned_data['repay_datetime']
        #     # 将前端传过来的时间格式化为日期类型
        #     r_date = repay_datetime.date()
        #
        #     # 获取当前时间
        #     now_date = datetime.date.today()
        #     if repay_datetime is u"" or r_date <= now_date:
        #         msg = u"还款日期必须比借款日期晚!"
        #         self._errors['repay_datetime'] = self.error_class([msg])
        #
        #         del cleaned_data['repay_datetime']

        return cleaned_data
        # 家庭借入信息后端check结束

    def __init__(self, *args, **kwargs):
        super(BorrowForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Borrow
        fields = ('borrow_amount', 'balance', 'borrow_person', 'lend_person', 'repay_datetime',
                  'borrow_datetime', 'remarks')


class Lend(models.Model):
    """
    家庭流水管理之--借出
    """
    user = models.ForeignKey(User, verbose_name=u"家庭借出管理信息登记人", blank=True, null=True, related_name='user_lend')
    lend_amount = models.DecimalField(u'借出金额', max_digits=8, decimal_places=2, default=0)  # 借出金额
    balance = models.DecimalField(u'账户余额', max_digits=8, decimal_places=2, default=0)  # 账户余额
    borrow_person = models.CharField(u"借入人", max_length=255)  # 这个字段标识谁借了这笔款项
    lend_person = models.CharField(u"借出人", max_length=255)  # 这个字段标志了谁将这笔款项借出的
    handler = models.CharField(u"信息记录人", max_length=255)  # 谁记录了这条记录
    lend_datetime = models.DateTimeField()  # 借出日期
    pay_datetime = models.DateTimeField()  # 预计还款日期
    update_datetime = models.DateTimeField(auto_now=True)  # 更新日期
    remarks = models.TextField(u"备注", null=True, blank=True)  # 备注的添加用于描述这笔借款的具体来源和数量描述
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = 'graduation_design_lend'


class LendForm(ModelForm):
    """
    家庭借出信息表单提交Form
    """
    def clean(self):
        cleaned_data = super(LendForm, self).clean()
        # 家庭借入信息后端check开始
        if 'borrow_person' in cleaned_data:
            borrow_person = cleaned_data['borrow_person']
            if borrow_person is u"":
                msg = u"借款人不可以为空,默认为当前登录用户!"
                self._errors['borrow_person'] = self.error_class([msg])

                del cleaned_data['borrow_person']

        if 'lend_person' in cleaned_data:
            lend_person = cleaned_data['lend_person']
            if lend_person is u"" or lend_person.isdigit():
                msg = u"借出款人不可以为空,且必须为有效的名字!!"
                self._errors['lend_person'] = self.error_class([msg])

                del cleaned_data['lend_person']

        if 'lend_amount' in cleaned_data:
            lend_amount = cleaned_data['lend_amount']
            amount = float(lend_amount)
            if lend_amount is u"" or amount <= 0:
                msg = u"请填入有效的借出金额(例如:100,单位默认为元)!!"
                self._errors['borrow_amount'] = self.error_class([msg])

                del cleaned_data['lend_amount']

        if 'balance' in cleaned_data:
            balance = cleaned_data['balance']
            amount = float(balance)
            if balance is u"" or amount < 0:
                msg = u"余额再怎么少,也不可能小雨0吧!"
                self._errors['balance'] = self.error_class([msg])

                del cleaned_data['balance']

        # if 'lend_datetime' in cleaned_data:
        #     lend_datetime = cleaned_data['lend_datetime']
        #     # 前端传过来的时间,将其格式化为日期格式
        #     b_date = lend_datetime.date()
        #     # 获取当前日期
        #     n_date = datetime.date.today()
        #
        #     if lend_datetime is u"" or b_date > n_date:
        #         msg = u"请选择有效的借入时间(借出时间不可以大于当前时间)!!"
        #         self._errors['lend_datetime'] = self.error_class([msg])
        #
        #         del cleaned_data['lend_datetime']
        #
        # if 'pay_datetime' in cleaned_data:
        #     pay_datetime = cleaned_data['pay_datetime']
        #     p_date = pay_datetime.date()
        #
        #     # 获取当前时间
        #     n_date = datetime.date.today()
        #
        #     if pay_datetime is u"" or p_date <= n_date:
        #         msg = u"请填写合理的还款日期(还款日期必须小于等于当前时间!)!!"
        #         self._errors['pay_datetime'] = self.error_class([msg])
        #
        #         del cleaned_data['pay_datetime']

        return cleaned_data
        # 家庭借入信息后端check结束

    def __init__(self, *args, **kwargs):
        super(LendForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Lend
        fields = ('lend_amount', 'balance', 'borrow_person', 'lend_person', 'pay_datetime',
                  'lend_datetime', 'remarks')


