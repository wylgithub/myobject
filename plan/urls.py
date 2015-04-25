#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wyl'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('plan.views',

    #  周流水计划开始
    # url(r'^week/add/(\d+)/$', 'week_add_view'),
    # url(r'^week/(\d+)/add/action/$', 'week_add_action'),
    # url(r'^week/list/$', 'week_list_view'),
    # url(r'^week/delete/list/$', 'week_delete_action'),
    #  周流水计划结束

    #  月流水计划开始
    url(r'^month/add/(\d+)/$', 'month_add_view'),
    url(r'^month/(\d+)/add/action/$', 'month_add_action'),
    url(r'^month/list/$', 'month_list_view'),
    url(r'^month/delete/list/$', 'month_delete_action'),
    #  月流水计划结束

    #  年流水计划开始
    url(r'^year/add/(\d+)/$', 'year_add_view'),
    url(r'^year/(\d+)/add/action/$', 'year_add_action'),
    url(r'^year/list/$', 'year_list_view'),
    url(r'^year/delete/list/$', 'year_delete_action'),
    # 年流水计划结束

    )

