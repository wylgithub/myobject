# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

__author__ = 'wyl'

urlpatterns = patterns('income.views',

    url(r'^add/$', 'add_income_view'),  # 添加收入明细view
    url(r'^list/$', 'income_list_view'),  # 收入明细一览view

)