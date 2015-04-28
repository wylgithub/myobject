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

    # 家庭收入编辑开始
    url(r'^edit/(\d+)/income/(\d+)/$', 'income_edit_view'),
    url(r'^edit/action/$', 'income_edit_action'),
    url(r'^delete/action/$', 'income_delete_action'),
    # 家庭编辑完成

    # 家庭支出信息编辑开始(只增加删除功能,编辑功能等有时间再做)
    url(r'^expend/edit/(\d+)/expend/(\d+)/$', 'expend_edit_view'),
    url(r'^expend/edit/action/$', 'expend_edit_action'),
    url(r'expend/delete/action/', 'expend_delete_action'),
    # 家庭支出信息编辑结束

    # 家庭借入信息模块开始:
    url(r'^borrow/add/(\d+)/$', 'add_borrow_view'),  # 添加借入明细view
    url(r'^borrow/(\d+)/add/action/$', 'add_borrow_action'),  # 添加借入明细action
    url(r'^borrow/list/$', 'borrow_list_view'),  # 借入信息一览view
    url(r'^borrow/delete/action/$', 'borrow_delete_action'),  # 删除明细一览view
    # 家庭借入信息模块结束:


    # 家庭借出信息模块开始
    url(r'^lend/add/(\d+)/$', 'add_lend_view'),  # 添加借出明细view
    url(r'^lend/(\d+)/add/action/$', 'add_lend_action'),  # 添加借出明细action
    url(r'^lend/list/$', 'lend_list_view'),  # 借出信息一览view
    url(r'^lend/delete/action/$', 'lend_delete_action'),  # 删除明细一览view
    # 家庭借出信息模块结束

)