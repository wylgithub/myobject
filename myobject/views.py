#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponse

__author__ = 'wyl'


# 测试模板的访问----测试结果(OK)
def get_current_datetime(request):

    now = datetime.datetime.now()

    return render_to_response('current_datetime.html', {'current_now': now})