#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from user_account.models import UserLoginForm, UserForm, User
from django.contrib.auth import authenticate, login, logout
from utility.base_view import back_to_original_page, get_list_params
from utility.exception import PermissionDeniedError
from utility.role_manager import check_role, ROLE_FAMILY_SUPER_USER, ROLES, ROLE_FAMILY_COMMON_USER, ROLE_SYSADMIN, \
    ROLE_MEMBER
from utility import role_manager


def login_view(request):
    """
    登录view
    """
    return render(request, "user_account/login.html")


def login_action(request):
    """
    登录动作
    :param request:
    :return:
    """
    form = UserLoginForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        if cleaned_data. has_key('needRemember') and cleaned_data['needRemember']:
            request.session.set_expiry(2678400)  # session保持一个月

        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return back_to_original_page(request, "/")

    return render(request, "user_account/login.html", {
        "form": form,
    })


def logout_action(request):
    """
    注销动作
    """
    logout(request)
    return redirect(settings.LOGIN_URL)


# 用户这侧模块开始
def register_view(request):
    """
    注册初期话View
    author:ganfeng
    added by 2013/04/23
    """

    form = UserForm()

    # challenge, response = captcha.conf.settings.get_challenge()()
    # store = CaptchaStore.objects.create(challenge=challenge, response=response)
    # CaptchaStore.generate_key()

    return render(request, "user_account/register.html", {
        "form": form,
        # "captcha_key": store.hashkey
    })


def register_action(request):
    """
    用户注册
    """
    form = UserForm(request.POST)

    if form.is_valid():

        reg_user = form.save()
        reg_user.set_password(form.cleaned_data['password'])
        ip = request.META.get('REMOTE_ADDR')
        reg_user.last_login_ip = ip
        reg_user.save()

        # 登录操作
        cleaned_data = form.cleaned_data

        user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
        # 直接登录该用户
        login(request, user)

        return render(request, "account/reg.html", {
            "form": form,
        })

#  用户注册模块结束


# 用户维护模块开始
@login_required
def user_add_view(request):
    """
    增加用户View
    """
    form = UserForm()
    return render(request, "user_account/add.html", {
        "form": form,
    })


@login_required
def user_add_action(request):
    """
    增加用户
    """
    if check_role(request, ROLE_FAMILY_COMMON_USER):
        raise PermissionDeniedError

    form = UserForm(request.POST)

    if form.is_valid():

        # 家庭管理员只能添加家庭普通成员
        role = form.cleaned_data['role']
        if check_role(request, ROLE_FAMILY_SUPER_USER) and role != ROLE_FAMILY_COMMON_USER:
            msg = u"家庭管理员只能添加家庭普通成员。"
            form._errors["role"] = form.error_class([msg])
            return render(request, "user_account/add.html", {
                "form": form,
            })
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        group = role_manager.get_role(role)

        # 添加用户到组
        if group:
            user.groups.add(group)
        user.save()  # 保存用户到数据库
        return back_to_original_page(request, "/user_account/list/")
    else:
        return render(request, "user_account/add.html", {
            "form": form,
        })


@login_required
def user_list_view(request):
    """
    用户一览View
    """
    queryset = User.objects.filter(is_superuser=False).exclude(is_active=False)
    params = get_list_params(request)

    order_dict = {
        u"un": "username",
        u"fn": "full_name",
        u"cd": "create_datetime",
        u"gr": "groups",
        u"ci": "city_id",
    }

    # 搜索条件
    if params['query']:
        queryset = queryset.filter(username__contains=params['query'])

    # 如果是超级管理员,那么显示所有的用户信息
    if check_role(request, ROLE_SYSADMIN):
        queryset = queryset

    # 如果是家庭管理员,那么只显示家庭普通成员的信息
    elif check_role(request, ROLE_FAMILY_SUPER_USER):
        queryset = queryset.filter(groups__name=ROLES[ROLE_FAMILY_COMMON_USER])

    # 如果是注册会员,那么可以看到一些付费功能
    # elif check_role(request, ROLE_MEMBER):
    #     queryset = queryset

    # 排序
    if not params['order_field'] or not order_dict. has_key(params['order_field']):
        params['order_field'] = 'un'
        params['order_direction'] = ''

    queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))
    total_count = queryset.count()

    return render(request, "user_account/list.html", {
        "users": queryset[params['from']:params['to']],
        "query_params": params,
        "need_pagination": params['limit'] < total_count,
        "total_count": total_count,
    })

#
# @login_required
# def user_delete_action(request):
#     """
#     删除用户
#     """
#     if check_role(request, ROLE_CHANNEL_MANAGER) or check_role(request, ROLE_SALES_MANAGER):
#         raise PermissionDeniedError
#
#     if not request.POST.has_key('pk'):
#         raise InvalidPostDataError()
#     pk = request.POST["pk"]
#     pks = []
#     for key in pk.split(','):
#         if key and is_int(key):
#             pks.append(int(key))
#
#     User.objects.filter(id__in=pks).update(is_active=False)
#     return back_to_original_page(request, '/epiao_account/list/')
#
# # 用户维护模块结束