#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from income.models import IncomeForm, Income, ExpendForm, Expend
from user_account.models import User
from utility.base_view import back_to_original_page, get_list_params


# 添加收入信息模块开始
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

    else:
        return render_to_response("income/add_income.html", {
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

# 收入信息模块完成


# 支出模块开始
@login_required
def add_expend_view(request, user_id):
    """
    添加支出信息
    :param request:
    :param user_id:
    :return:
    """
    id = int(user_id)

    # 获取当前登录用户
    user = User.objects.filter(id=id).get()
    # 获取登录用户的全名
    full_name = user.full_name

    # 获取登录用户的用户名
    username = user.username

    # 获取当前登录用户的身份
    user_identity = u''
    if user.groups.count() > 0:
        user_identity = user.groups.get().name

    return render(request, "income/add_expend.html", {
        'user_id': id,
        'full_name': full_name,
        'username': username,
        'identity': user_identity,
    })


@login_required
def add_expend_action(request, user_id):
    """
    添加支出信息action
    :param request:
    :param user_id:
    :return:
    """
    # 将登录用户id进行格式化
    id = int(user_id)

    # 获取前端提交的信息
    form = ExpendForm(request.POST, instance=Expend())

    if form.is_valid():
        # 将用户id报错到user_id字段
        form.instance.user_id = id
        form.save()

        return back_to_original_page(request, "/income/expend/list/")

    else:
        return render(request, "income/add_expend.html", {
            'form': form,
        })


@login_required
def expend_list_view(request):

    # 获取收入信息的queryset
    queryset = Expend.objects.filter()

    # 获取收入信息实例
    expends = queryset

    # 排序
    params = get_list_params(request)

    order_dict = {
        u"type": "income_type",
        u"acc": "income_amount",
        u"amo": "create_datetime",
        u"amc": "handler",
        u"tm": "remarks",
        u"hl": "remarks",
        u"mk": "remarks",
        u"tm": "remarks",
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
        'expends': expends,

    })

# 支出模块结束