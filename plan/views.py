#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from plan.models import Weekly, Monthly, Yearly, MonthlyForm, YearlyForm
from user_account.models import User
from utility.base_view import back_to_original_page, get_list_params
from utility.constant import DATE_INPUT_FORMAT_HYPHEN
from utility.datetime_utility import get_today
from utility.exception import PermissionDeniedError
from utility.role_manager import check_role, ROLE_FAMILY_COMMON_USER


def family_plan_view(request, id):
    """
    家庭流水计划信息views
    :param request:
    :param id:
    :return:
    """
    user_id = int(id)
    # 获取一个用户实例
    user = User.objects.filter(id=user_id).get()

    # 获取登录用户的角色名
    role_name = None
    if user.groups.count() > 0:
        role_name = user.groups.get().name

    # 获取周流水计划信息
    week_count = Weekly.objects.filter(delete_flg=False).count()
    week_list = Weekly.objects.filter(delete_flg=False).order_by("work_income")

    # 获取月流水计划信息
    monthly_count = Monthly.objects.filter().exclude(delete_flg=False).count()
    monthly_list = Monthly.objects.filter().exclude(delete_flg=False).order_by('work_income')

    # 获取年流水计划信息
    yearly_count = Yearly.objects.filter().exclude(delete_flg=False).count()
    yearly_list = Yearly.objects.filter().exclude(delete_flg=False).order_by('work_income')

    return render(request, "plan/plan.html", {
        'id': user_id,
        'role_name': role_name,
        'full_name': user.full_name,
        'week_count': week_count,
        'week_list': week_list,
        'monthly_count': monthly_count,
        'monthly_list': monthly_list,
        'yearly_count': yearly_count,
        'yearly_list': yearly_list,
    })


# 月预算信息添加开始
@login_required
def month_add_view(request, user_id):
    """
    添加借入明细view
    :param request:
    :param user_id:
    :return:
    """
    id = int(user_id)
    user = User.objects.filter(id=id).get()

    user_name = u''
    if user.groups.count() > 0:
        user_name = user.groups.get().name

    return render(request, "plan/add_monthly.html", {
        'user_id': id,
        'username': user.full_name,
        'user_type': user_name,
        'current_now': get_today().strftime(DATE_INPUT_FORMAT_HYPHEN),
    })



@login_required
def month_add_action(request, user_id):
    """
    添加借入信息action
    :param request:
    :param user_id:
    :return:
    """
    # 将登录用户id进行格式化
    id = int(user_id)
    user = User.objects.filter(id=id).get()

    # 获取登录人姓名
    username = user.full_name
    # 获取前端提交的信息
    form = MonthlyForm(request.POST, instance=Monthly())

    if form.is_valid():
        # 将用户id保存到user_id字段
        form.instance.user_id = id
        form.instance.handler = username
        form.save()

        return back_to_original_page(request, "/plan/month/list/")
    else:
        return render(request, "plan/add_monthly.html", {
            'form': form,
            'user_id': id,
            'username': username,
            'current_now': get_today().strftime(DATE_INPUT_FORMAT_HYPHEN),
        })


@login_required
def month_list_view(request):
    """
    收入明细一览表
    :param request:
    :return:
    """
    # 获取收入信息的queryset
    queryset = Monthly.objects.filter().exclude(delete_flg=True)

    # 获取收入信息实例
    months = queryset

    # 排序
    params = get_list_params(request)

    order_dict = {
        u"op": "handler",
        u"jr": "work_income",
        u"jc": "investment_income",
        u"jj": "life_spend",
        u"ky": "other_spend",
        u"jq": "start_date",
        u"hq": "end_date",
        u"mk": "remarks",
    }

    # 搜索条件
    if params['query']:
        queryset = queryset.filter(work_income__contains=params['query'])

    # 排序
    if not params['order_field'] or not order_dict. has_key(params['order_field']):
        params['order_field'] = 'jj'
        params['order_direction'] = ''

    queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))
    total_count = queryset.count()

    return render(request, "plan/monthly_list.html", {
        'months': queryset[params['from']: params['to']],
        'query_params': params,
        'need_pagination': params['limit'] < total_count,
        'total_count': total_count,
        'month': months,

    })


@login_required
def month_delete_action(request):
    """
    家庭借入信息删除action
    :param request:
    :return:
    """
    # 如果是家庭普通成员则报错
    if check_role(request, ROLE_FAMILY_COMMON_USER):
        raise PermissionDeniedError

    pk = request.POST["pk"]
    pks = []
    for key in pk.split(','):
        if key:
            pks.append(int(key))

    Monthly.objects.filter(id__in=pks).update(delete_flg=True, update_datetime=datetime.now())
    return back_to_original_page(request, '/plan/month/list/')

# 月预算信息添加结束

# 年预算信息添加开始
@login_required
def year_add_view(request, user_id):
    """
    添加借入明细view
    :param request:
    :param user_id:
    :return:
    """
    id = int(user_id)
    user = User.objects.filter(id=id).get()

    user_name = u''
    if user.groups.count() > 0:
        user_name = user.groups.get().name

    return render(request, "plan/add_yearly.html", {
        'user_id': id,
        'username': user.full_name,
        'user_type': user_name,
        'current_now': get_today().strftime(DATE_INPUT_FORMAT_HYPHEN),
    })



@login_required
def year_add_action(request, user_id):
    """
    添加借入信息action
    :param request:
    :param user_id:
    :return:
    """
    # 将登录用户id进行格式化
    id = int(user_id)
    user = User.objects.filter(id=id).get()

    # 获取登录人姓名
    username = user.full_name
    # 获取前端提交的信息
    form = YearlyForm(request.POST, instance=Yearly())

    if form.is_valid():
        # 将用户id保存到user_id字段
        form.instance.user_id = id
        form.instance.handler = username
        form.save()

        return back_to_original_page(request, "/plan/year/list/")
    else:
        return render(request, "plan/add_yearly.html", {
            'form': form,
            'user_id': id,
            'username': username,
            'current_now': get_today().strftime(DATE_INPUT_FORMAT_HYPHEN),
        })


@login_required
def year_list_view(request):
    """
    收入明细一览表
    :param request:
    :return:
    """
    # 获取收入信息的queryset
    queryset = Yearly.objects.filter().exclude(delete_flg=True)

    # 获取收入信息实例
    years = queryset

    # 排序
    params = get_list_params(request)

    order_dict = {
        u"op": "handler",
        u"jr": "work_income",
        u"jc": "investment_income",
        u"jj": "life_spend",
        u"ky": "other_spend",
        u"jq": "start_date",
        u"hq": "end_date",
        u"mk": "remarks",
    }

    # 搜索条件
    if params['query']:
        queryset = queryset.filter(work_income__contains=params['query'])

    # 排序
    if not params['order_field'] or not order_dict. has_key(params['order_field']):
        params['order_field'] = 'jj'
        params['order_direction'] = ''

    queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))
    total_count = queryset.count()

    return render(request, "plan/yearly_list.html", {
        'years': queryset[params['from']: params['to']],
        'query_params': params,
        'need_pagination': params['limit'] < total_count,
        'total_count': total_count,
        'year': years,
    })


@login_required
def year_delete_action(request):
    """
    家庭借入信息删除action
    :param request:
    :return:
    """
    # 如果是家庭普通成员则报错
    if check_role(request, ROLE_FAMILY_COMMON_USER):
        raise PermissionDeniedError

    pk = request.POST["pk"]
    pks = []
    for key in pk.split(','):
        if key:
            pks.append(int(key))

    Yearly.objects.filter(id__in=pks).update(delete_flg=True, update_datetime=datetime.now())
    return back_to_original_page(request, '/plan/year/list/')

# 月预算信息添加结束
