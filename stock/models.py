#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

from user_account.models import User


class Stock(models.Model):
    """
    股票交易记录
    """
    user = models.ForeignKey(User, verbose_name=u"股票信息记录", blank=True, null=True, related_name='user_stock')
    stock_label = models.CharField(u"股票代号", max_length=10) # 股票代码
    stock_name = models.CharField(u"股票中文名字", max_length=10) # 股票的中文名称
    buy_date = models.DateTimeField(u"股票买入日期") # 股票的买入日期
    sold_date = models.DateTimeField(u"股票卖出日期")  # 股票的预计卖出日期
    update_date = models.DateTimeField(u"股票信息更新日期", auto_now_add=True)  # 股票信息更新日期
    buy_amount = models.IntegerField(u"股票买入手数", max_length=10) # 股票的买入数量
    buy_price = models.DecimalField(u"股票的买入价格", max_digits=10, decimal_places=2) # 股票买入的价格
    sold_price = models.DecimalField(u"股票的预计卖出价格", max_digits=10, decimal_places=2) # 股票卖出的价格
    stop_lose_price = models.DecimalField(u"止损价格", max_length=10, max_digits=10, decimal_places=2)  # 止损价格
    earn = models.DecimalField(u"本次投资预计收益", max_digits=10, decimal_places=2) # 本次投资预计收益
    handler = models.CharField(u"添加股票交易处理者", max_length=255)  # 处理者:添加支出信息的人
    remarks = models.TextField(u"备注", max_length=500)  # 备注的添加用于描述此次股票交易相关
    delete_flg = models.BooleanField(default=False)  # 删除标志位

    class Meta:
        db_table = 'graduation_design_stock'


class StockForm(ModelForm):
    """
    工作经历Form
    """

    def clean(self):
        cleaned_data = super(StockForm, self).clean()

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Stock
        fields = ('stock_label', 'stock_name', 'buy_date', 'sold_date', 'buy_amount', 'buy_price', 'sold_price',
                  'stop_lose_price', 'earn', 'handler', 'remarks')