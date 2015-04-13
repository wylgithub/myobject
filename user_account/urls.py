#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

__author__ = 'wyl'

urlpatterns = patterns('user_account.views',

    url(r'^login/$', "login_view"),
    url(r'^login/action/$', "login_action"),
    url(r'^logout/$', "logout_action"),
)