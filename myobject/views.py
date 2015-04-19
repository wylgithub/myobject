#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render


__author__ = 'wyl'


@login_required
def index_view(request):
    """
    首页View
    """
    # 如果是影院账户，则跳转到专用画面
    login_user = request.user

    return render(request, "index/index.html", {
        'user': login_user
    })