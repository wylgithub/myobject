#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


__author__ = 'wyl'


# 测试模板的访问----测试结果(OK)
@login_required
def get_current_datetime(request):

    now = datetime.datetime.now()

    return render_to_response('index/index.html', {'current_now': now})