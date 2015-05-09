#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from income.models import Income, Expend, Borrow, Lend


@login_required
def get_total_list_view(request):

    # 收入信息接受对象
    income_list = []
    total_income = 0

    # 支出信息接受对象
    expend_list = []
    total_expend = 0

    # 借入信息接受对象
    borrow_list = []
    total_borrow = 0

    # 借出信息接受对象
    lend_list = []
    total_lend = 0

    # 获取家庭收入信息汇总
    income_queryset = Income.objects.filter(delete_flg=False)

    # 获取收入金额存于列表
    for income in income_queryset:
        income_list.append(int(income.income_amount))
    # 获取总收入
    for amount in income_list:
        total_income += amount

    # 获取家庭之处信息汇总
    expend_queryset = Expend.objects.filter(delete_flg=False)

    for expend in expend_queryset:
        expend_list.append(int(expend.expend_account))

    for amount in expend_list:
        total_expend += amount

    # 获取家庭借入信息汇总
    borrow_queryset = Borrow.objects.filter(delete_flg=False)

    for borrow in borrow_queryset:
        borrow_list.append(int(borrow.borrow_amount))

    for amount in borrow_list:
        total_borrow += amount

    # 获取家庭借出信息汇总
    lend_queryset = Lend.objects.filter(delete_flg=False)

    for lend in lend_queryset:
        lend_list.append(int(lend.lend_amount))

    for amount in lend_list:
        total_lend += amount

    return render(request, "get_total/get_total_list.html", {
        "total_income": total_income,
        "total_expend": total_expend,
        "total_borrow": total_borrow,
        "total_lend": total_lend,
    })
