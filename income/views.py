#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from income.models import IncomeForm, Income
from user_account.models import User
from utility.base_view import back_to_original_page, get_list_params
from utility.constant import DATE_INPUT_FORMAT_HYPHEN, DATE_TIME_FORMATS, DATE_INPUT_FORMATS, JSON_ERROR_CODE_NO_ERROR


@login_required
def add_income_view(request, user_id):
    """
    添加收入明细view
    :param request:
    :return:
    """
    # form = IncomeForm()
    # 获取用户对象实例
    id = int(user_id)
    user = User.objects.filter(id=id).get()

    user_name = u''
    if user.groups.count() > 0:
        user_name = user.groups.get().name

    # 获取操作人员
    # income_info = Income.objects.filter(id=id)

    return render(request, "income/add_income.html", {
        'user_id': id,
        'username': user.full_name,
        'user_type': user_name
    })


@login_required
def add_income_action(request, user_id):
    """
    添加收入明细action
    :param request:
    :return:
    """
    id = int(user_id)

    form = IncomeForm(request.POST)

    if form.is_valid():

        # 获取用户名报讯到数据库
        user = User.objects.filter(id=id).get()

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
        mark_name = user.full_name

        Income.objects.create(income_type=income_type,
                              create_datetime=get_add_date,
                              income_amount=income_amount,
                              remarks=remark,
                              handler=mark_name,
                              user_id=id,
                              )

        return back_to_original_page(request, "/income/list/")
        # return render_to_response("income/add_income.html", {
        #         'result': 'OK',
        #         'error_code': JSON_ERROR_CODE_NO_ERROR,
        #         'validation': True,
        #         'form': form,
        #         'username': mark_name
        #         },  context_instance=RequestContext(request))
    else:
        return render_to_response("income/add_income.html", {
            'result': 'OK',
            'error_code': JSON_ERROR_CODE_NO_ERROR,
            'validation': False,
            'form': form,
        }, context_instance=RequestContext(request))



@login_required
def income_list_view(request):
    """
    收入明细一览表
    :param request:
    :return:
    """
    # 获取收入信息的queryset
    queryset = Income.objects.filter()

    # 获取收入信息实例
    incomes = queryset

    # 排序
    params = get_list_params(request)

    order_dict = {
        u"ty": "income_type",
        u"am": "income_amount",
        u"tm": "create_datetime",
        u"hl": "handler",
        u"mk": "remarks",
    }

    # 搜索条件
    if params['query']:
        queryset = queryset.filter(income_type__contains=params['query'])

    # 排序
    if not params['order_field'] or not order_dict. has_key(params['order_field']):
        params['order_field'] = 'am'
        params['order_direction'] = ''

    queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))
    total_count = queryset.count()

    return render(request, "income/income_detail.html", {
        'incomes': queryset[params['from']: params['to']],
        'query_params': params,
        'need_pagination': params['limit'] < total_count,
        'total_count': total_count,
        'income': incomes,

    })
