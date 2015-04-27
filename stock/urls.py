#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wyl'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('stock.views',
    # 个人信息
    url(r'^personal/financial/(\d+)/$', 'personal_financial_view'),

    url(r'^personal/(\d+)/stock/list/$', 'stock_list_view'),  # 工作一览view
    url(r'^personal/(\d+)/stock/edit/(\d+)/$', 'stock_edit_view'),  # 工作编辑view
    url(r'^personal/(\d+)/stock/edit/action/$', 'stock_edit_action'),  # 工作编辑action
    url(r'^personal/(\d+)/stock/add/$', 'stock_add_view'),  # 股票添加view
    url(r'^personal/(\d+)/stock/delete/action/$', 'stock_delete_action'),  # 工作删除action
)