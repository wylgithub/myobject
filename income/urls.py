# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

__author__ = 'wyl'

urlpatterns = patterns('income.views',

    # 收入信息记录开始
    url(r'^add/(\d+)/$', 'add_income_view'),  # 添加收入明细view
    url(r'^(\d+)/add/action/$', 'add_income_action'),  # 添加收入明细action
    url(r'^list/$', 'income_list_view'),  # 收入明细一览view]
    # 收入信息记录完成

    # 支出信息记录
    url(r'^expend/add/(\d+)/$', 'add_expend_view'),  # 添加收入明细view
    url(r'^expend/(\d+)/add/action/$', 'add_expend_action'),  # 添加收入明细action
    url(r'^expend/list/$', 'expend_list_view'),  # 收入明细一览view
    # 支出信息记录完成


)