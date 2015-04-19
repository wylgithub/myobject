#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from income.models import IncomeForm, Income
from utility.constant import DATE_INPUT_FORMAT_HYPHEN, DATE_TIME_FORMATS, DATE_INPUT_FORMATS, JSON_ERROR_CODE_NO_ERROR


@login_required
def add_income_view(request):
    """
    添加收入明细view
    :param request:
    :return:
    """
    form = IncomeForm()

    return render(request, "income/add_income.html", {
        'form': form,
    })


@login_required
def add_income_action(request):
    """
    添加收入明细action
    :param request:
    :return:
    """
    form = IncomeForm(request.POST)

    if form.is_valid():

        print(request.POST['recode_date'])
        # 将前端传入的时间格式化为日期
        # get_add_date = to_date(request.POST['recode_date'], DATE_TIME_FORMATS)
        get_add_date = request.POST['recode_date']
        # 收入类型
        income_type = request.POST['income_type']
        # 收入金额:将前端传入的unicode金额类型转换成float型
        income_amount = float(request.POST['income_amount'])
        # 标识字段
        remark = request.POST['remark']
        # 信息登记人
        mark_name = request.POST['recode_name']

        Income.objects.create(income_type=income_type,
                              create_datetime=get_add_date,
                              income_amount=income_amount,
                              remarks=remark,
                              handler=mark_name,)
        return render_to_response("income/add_income.html", {
                'result': 'OK',
                'error_code': JSON_ERROR_CODE_NO_ERROR,
                'validation': True,
                'form': form,
                },  context_instance=RequestContext(request))
    else:
        return render_to_response("income/add_income.html", {
            'result': 'OK',
            'error_code': JSON_ERROR_CODE_NO_ERROR,
            'validation': False,
            'form': form,
        }, context_instance=RequestContext(request))

    # return render(request, "income/add_income.html", {
    #                 'form': form,
    #                 'validation': True
    #                 })


@login_required
def income_list_view(request):
    """
    收入明细一览表
    :param request:
    :return:
    """

    return render(request, "income/income_detail.html", {

    })
