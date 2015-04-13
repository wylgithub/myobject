#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse

__author__ = 'wyl'


# 测试模板的访问----测试结果(OK)
@login_required
def get_current_datetime(request):

    now = datetime.datetime.now()

    return render_to_response('index.html', {'current_now': now})