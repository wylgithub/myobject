#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

__author__ = 'wyl'

urlpatterns = patterns('user_account.views',

    # 用户维护开始
    url(r'^add/$', 'user_add_view'),
    url(r'^add/action/$', 'user_add_action'),
    url(r'^list/$', 'user_list_view'),
    # 用户维护结束


    # 用户登录模块开始
    url(r'^login/$', "login_view"),
    url(r'^login/action/$', "login_action"),
    url(r'^logout/$', "logout_action"),
    #  用户登录模块结束

    #  用户注册模块
    url(r'^register/$', 'register_view'),  # 显示登录页面
    url(r'^register/action/$', 'register_action'),  # 进行登录提交

)