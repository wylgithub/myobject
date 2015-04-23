#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext

from user_account.models import UserLoginForm, UserForm, User, UserEditForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from utility.base_view import back_to_original_page, get_list_params
from utility.constant import JSON_ERROR_CODE_NO_ERROR
from utility.exception import PermissionDeniedError
from utility.role_manager import check_role, ROLE_FAMILY_SUPER_USER, ROLES, ROLE_FAMILY_COMMON_USER, ROLE_SYSADMIN, \
    ROLE_MEMBER, check_permission_allowed, get_role_id
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

    form = UserRegisterForm()

    return render(request, "user_account/register.html", {
        "form": form,
    })


def register_action(request):
    """
    用户注册
    """
    response_data = {}
    try:
        form = UserRegisterForm(request.POST, instance=User())
        if form.is_valid():

            role = form.cleaned_data['role']
            form.instance.username = request.POST['username']
            form.instance.password = request.POST['password']
            form.instance.full_name = request.POST['full_name']
            form.instance.email = request.POST['email']
            form.instance.mobile = request.POST['mobile']

            user = form.save()
            user.set_password(form.instance.password)
            group = role_manager.get_role(role)

            if group:
                user.groups.add(group)
            user.save()
            return render_to_response("user_account/register.html", {
                'result': 'OK',
                'error_code': JSON_ERROR_CODE_NO_ERROR,
                'validation': True,
                'form': form,
            }, context_instance=RequestContext(request))

        else:
            return render_to_response("user_account/register.html", {
                'result': 'OK',
                'error_code': JSON_ERROR_CODE_NO_ERROR,
                'validation': False,
                'goods': form,
            }, context_instance=RequestContext(request))

    except:
        response_data['validate'] = True
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
#  用户注册模块结束


# 用户维护模块开始
@login_required
def user_add_view(request):
    """
    增加用户View
    """

    if check_role(request, ROLE_FAMILY_COMMON_USER):
        raise PermissionDeniedError

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
        u"mb": "mobile",
        u"em": "email",
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


@login_required
def user_view_view(request, id):
    """
    查看用户视图
    """
    if not check_permission_allowed(request, id):
        raise PermissionDeniedError

    user = get_object_or_404(User, id=id)
    role_name = None
    if user.groups.count() > 0:
        role_name = user.groups.get().name
    form = UserForm(instance=user)
    role_id = get_role_id(role_name) if role_name else None

    return render(request, "user_account/view.html", {
        "form": form,
        "role": role_id,
        "role_name": role_name,
    })


@login_required
def user_delete_action(request):
    """
    删除用户
    """
    if check_role(request, ROLE_FAMILY_COMMON_USER):
        raise PermissionDeniedError

    pk = request.POST["pk"]
    pks = []
    for key in pk.split(','):
        # if key and is_int(key):
        if key:
            pks.append(int(key))

    User.objects.filter(id__in=pks).update(is_active=False)
    return back_to_original_page(request, '/user_account/list/')


@login_required
def user_edit_view(request, id):
    """
    编辑用户视图
    """
    user = get_object_or_404(User, id=id)

    form = UserForm(instance=user)
    if user.groups.count() > 0:
        role_name = user.groups.get().name
    else:
        role_name = None
    return render(request, "user_account/edit.html", {
        "form": form,
        "id": id,
        "role": get_role_id(role_name),
        "role_name": role_name,
    })


@login_required
def user_edit_action(request):
    """
    编辑用户动作
    """
    # if not request.POST.has_key('id'):
    #     raise InvalidPostDataError()
    id = request.POST['id']

    if not check_permission_allowed(request, id):
        raise PermissionDeniedError

    user = get_object_or_404(User, id=id)

    if request.POST.has_key('password'):
        form = UserForm(request.POST, instance=user)
    else:
        form = UserEditForm(request.POST, instance=user)

    if form.is_valid():
        # 数据一致性校验
        # if not 'update_timestamp' in request.POST or crypt.loads(request.POST["update_timestamp"]) != unicode(
        #         user.update_datetime):
        #     raise DataExclusivityError()
        if request.user.is_superuser:
            role = form.cleaned_data['role']
            group = role_manager.get_role(role)
            if group:
                user.groups.clear()
                user.groups.add(group)
        user.full_name = form.cleaned_data['full_name']

        if not isinstance(form, UserEditForm):
            user.set_password(form.cleaned_data['password'])
            user.save(update_fields=("full_name", "password", "update_datetime"))
        else:
            user.save(update_fields=("full_name", "update_datetime"))

        # 员工没有访问list权限,所以这里返回index
        if check_role(request, ROLE_FAMILY_COMMON_USER):
            return back_to_original_page(request, "/")
        return back_to_original_page(request, "/user_account/list/")
    else:
        role = form.cleaned_data['role'] if 'role' in form.cleaned_data else None
        return render(request, "user_account/edit.html", {
            "form": form,
            "id": id,
            "role": role,
            "role_name": ROLES[role] if role in ROLES else "",
            # "update_timestamp": crypt.encryt(unicode(user.update_datetime))
        })
