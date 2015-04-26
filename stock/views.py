#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from stock.models import Stock, StockForm
from user_account.models import User
from utility.constant import DATE_INPUT_FORMAT_HYPHEN
from utility.datetime_utility import get_today


@login_required
def personal_financial_view(request, id):
    """
    个人理财View
    """
    user_id = int(id)
    user = User.objects.filter(id=user_id).get()
    role_name = None
    if user.groups.count() > 0:
        role_name = user.groups.get().name

    stock = Stock.objects.filter()

    # 获取股票信息
    stock_count = stock.count()
    stock_list = stock.filter(delete_flg=False).order_by('buy_amount')

    return render(request, "stock/personal_fina.html", {
        "id": user_id,
        "full_name": user.full_name,
        "role_name": role_name,
        "form": stock,
        "stock_count": stock_count,
        "stock_list": stock_list,
    })


@login_required
def stock_add_view(request, user_pk):
    """
    添加股票信息views
    :param request:
    :return:
    """
    u_pk = int(user_pk)
    user = User.objects.filter(id=u_pk).get()

    user_name = u''
    if user.groups.count() > 0:
        user_name = user.groups.get().name

    form = StockForm()
    return render_to_response("stock/stock_add.html", {
        'result': 'OK',
        'user_name': user_name,
        'username': user.full_name,
        'user_pk': u_pk,
        'form': form,
        'current_now': get_today().strftime(DATE_INPUT_FORMAT_HYPHEN),
    }, context_instance=RequestContext(request))


@login_required
def stock_edit_action(request, user_pk):
    """
    编辑工作action
    """
    # 个人信息id
    user_id = int(user_pk)
    user = User.objects.filter(id=user_id).get()

    user_name = u''
    if user.groups.count() > 0:
        user_name = user.groups.get().name

    # 取得请求的工作信息id
    id = request.POST['id']

    if id == "":
        # 取得股票信息Form实例
        form = StockForm(request.POST, instance=Stock())
    else:
        # 取得股票信息
        queryset = Stock.objects.filter(id__exact=int(id), delete_flg=False)
        job = queryset.get()
        # 生成工作信息对应的Form实例
        form = StockForm(request.POST, instance=job)

    if form.is_valid():
        # 如果通过判断,保存数据到数据库

        form.instance.user_id = user_id
        form.save()

        return render_to_response("stock/stock_add.html", {
            'result': 'OK',
            'user_name': user_name,
            'username': user.full_name,
            'job_validation': True,
            'user_pk': user_pk,
            'form': form,
            'current_now': get_today().strftime(DATE_INPUT_FORMAT_HYPHEN),
        }, context_instance=RequestContext(request))
    else:
        return render_to_response("stock/stock_add.html", {
            'result': 'OK',
            'user_name': user_name,
            'username': user.full_name,
            'job_validation': False,
            'user_pk': user_pk,
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def stock_list_view(request, user_pk):
    # """
    # 工作一览View
    # """
    # if not check_permission_allowed(request, user_pk):
    #     raise PermissionDeniedError
    # # 个人信息id
    # user_id = int(user_pk)
    # # 取得个人信息
    # queryset = Personal.objects.filter(belong_to__id=user_id, delete_flg=False)
    # personal = queryset.get()
    #
    # # 工作信息
    # job_count = personal.job.filter(delete_flg=False).count()
    # job_list = personal.job.filter(delete_flg=False).order_by("start_date")
    #
    # return render_to_response("information/job_list.html", {
    #     'result': 'OK',
    #     'user_pk': user_pk,
    #     'job_count': job_count,
    #     'job_list': job_list,
    # }, context_instance=RequestContext(request))
    pass
