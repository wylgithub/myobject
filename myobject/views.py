#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, render
from income.models import Income, Expend, Lend, Borrow
from plan.models import Monthly, Yearly
from user_account.models import User
from utility.base_view import get_list_params



__author__ = 'wyl'


@login_required
def index_view(request):
    """
    首页View
    """
    # 用户一览queryset
    queryset = User.objects.filter(is_superuser=False).exclude(is_active=False)
    params = get_list_params(request)

    # 收入信息一览
    income_queryset = Income.objects.filter().exclude(delete_flg=True)
    income_params = get_list_params(request)

    # 获取收入信息的queryset
    expend_queryset = Expend.objects.filter().exclude(delete_flg=True)
    expend_params = get_list_params(request)

    # 借出queryset
    lend_queryset = Lend.objects.filter().exclude(delete_flg=True)

    # 排序
    lend_params = get_list_params(request)

    borrow_queryset = Borrow.objects.filter().exclude(delete_flg=True)
    # 排序
    borrow_params = get_list_params(request)


    month_queryset = Monthly.objects.filter().exclude(delete_flg=True)
    month_params = get_list_params(request)

    # 获取收入信息的queryset
    year_queryset = Yearly.objects.filter().exclude(delete_flg=True)
    year_params = get_list_params(request)

    return render(request, "index/index.html", {
        # 首页一览用户信息return开始
        "users": queryset[params['from']:params['to']],
        # 首页一览用户信息return结束
        # 收入信息
        'incomes': income_queryset[income_params['from']: income_params['to']],
        # 支出信息
        'expends': expend_queryset[expend_params['from']: expend_params['to']],
        # 借出
        'lends': lend_queryset[lend_params['from']: lend_params['to']],
        # 借入
        'borrows': borrow_queryset[borrow_params['from']: borrow_params['to']],
        # 月收入计划
        'months': month_queryset[month_params['from']: month_params['to']],
        # 年收入计划
        'years': year_queryset[year_params['from']: year_params['to']],
    })
