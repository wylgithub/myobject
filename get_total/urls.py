#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wyl'

from django.conf.urls import patterns, url


urlpatterns = patterns('get_total.views',

    # 支出信息记录
    # url(r'^expend/add/(\d+)/$', 'add_expend_view'),  # 添加收入明细view
    # url(r'^expend/(\d+)/add/action/$', 'add_expend_action'),  # 添加收入明细action

    url(r'^family/list/$', 'get_total_list_view'),  # 收入明细一览view
    # 支出信息记录完成
)