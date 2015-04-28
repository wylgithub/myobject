#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
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
    stock_count = stock.filter(delete_flg=False).count()
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
def stock_edit_view(request, user_pk, stock_id):
    """
    编辑工作view
    """
    # 取得用户id
    user_id = int(user_pk)
    # 取得用户信息
    user = User.objects.filter(id=user_id).get()

    # 取得用户信息
    user_type = u''
    if user.groups.count():
        user_type = user.groups.get().name

    # 取得登录用户的全名
    username = user.full_name

    # 取得股票记录信息id
    stock_id = int(stock_id)
    # 取得股票信息
    stock = Stock.objects.filter(id=stock_id, delete_flg=False)

    # 取得股票信息实例
    sto = stock.get()

    # 生成工作信息对应的Form实例
    stockForm = StockForm(instance=sto)

    return render_to_response("stock/stock_add.html", {
        'result': 'OK',
        'stock_id': stock_id,
        'username': username,
        'user_name': user_type,
        'user_pk': user_pk,
        'form': stockForm,
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

    # 取得请求的股票信息id
    id = request.POST['id']

    if id == "":
        # 取得股票信息Form实例
        form = StockForm(request.POST, instance=Stock())
    else:
        # 取得股票信息
        queryset = Stock.objects.filter(id__exact=int(id), user_id=user_id,  delete_flg=False)
        sto = queryset.get()
        # 生成股票对应的Form实例
        form = StockForm(request.POST, instance=sto)

    if form.is_valid():
        if id == "":
            # 如果通过判断,保存数据到数据库
            form.instance.user_id = user_id

            form.save()
        else:

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
            'current_now': get_today().strftime(DATE_INPUT_FORMAT_HYPHEN),
        }, context_instance=RequestContext(request))


@login_required
def stock_list_view(request, user_pk):
    """
    工作一览View
    """
    # 个人信息id
    user_id = int(user_pk)
    # 取得个人信息
    queryset = Stock.objects.filter(user_id=user_id, delete_flg=False)
    personal = queryset

    # 工作信息
    stock_count = personal.filter(delete_flg=False).count()
    stock_list = personal.filter(delete_flg=False)

    return render_to_response("stock/stock_list.html", {
        'result': 'OK',
        'user_pk': user_pk,
        'stock_count': stock_count,
        'stock_list': stock_list,
    }, context_instance=RequestContext(request))



@login_required
def stock_delete_action(request, user_pk):
    """
    删除股票记录信息action
    :param request:
    :param user_pk:
    :return:
    """
    user_id = int(user_pk)
    pks = []
    for key in request.POST["job_pks"].split(','):
        if key:
            pks.append(int(key))

    # 取得信息
    queryset = Stock.objects.filter(id__in=pks, delete_flg=False)

    # 将工作信息逻辑删除
    queryset.update(delete_flg=True, update_date=datetime.now())
    return render_to_response("stock/stock_list.html", {
        'result': 'OK',
        'user_pk': user_id,
    }, context_instance=RequestContext(request))
