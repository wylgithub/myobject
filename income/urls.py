# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

__author__ = 'wyl'

urlpatterns = patterns('income.views',

    url(r'^add/(\d+)/$', 'add_income_view'),  # 添加收入明细view
    url(r'^(\d+)/add/action/$', 'add_income_action'),  # 添加收入明细action
    url(r'^list/$', 'income_list_view'),  # 收入明细一览view

)