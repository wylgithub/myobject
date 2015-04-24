#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User

__author__ = 'wyl'

ROLE_SYSADMIN = 99
ROLE_FAMILY_SUPER_USER = 10
ROLE_MEMBER = 20
ROLE_FAMILY_COMMON_USER = 30

ROLES = {
    ROLE_SYSADMIN: u'系统管理员',  # 系统内的最大权限用户
    ROLE_MEMBER: u'会员',  # 这个角色用于后期代码扩展和功能添加后的收费角色
    ROLE_FAMILY_SUPER_USER: u'家庭管理员',  # 一个家庭有一个或者多个属于本家庭的超级管理员，用于管理本家庭的普通成员，存在一些权限操作
    ROLE_FAMILY_COMMON_USER: u'家庭普通成员',  # 家庭普通成员
}


# 根据角色组别的id获得文字描述
def get_role(role):
    if not role in ROLES:
        return None

    return Group.objects.get_or_create(name=ROLES[role])[0]


# 根据文字描述获得角色组别的id
def get_role_id(name):
    for k, v in ROLES.items():
        if v == name:
            return k
    return None


# 检查当前用户是否符合给定组别
def check_role(request, role):
    if role == ROLE_SYSADMIN and request.user.is_superuser:
        return True

    user = request.user
    return ROLES. has_key(role) and user.groups.filter(name=ROLES[role]).exists()


# 检查当前用户是否符合操作权限级别
# 既只能对自己或者低于自己权限用户进行操作
def check_permission_allowed(request, id):
    user = get_object_or_404(User, id=id)
    role_name = None
    if user.groups.count() > 0:
        role_name = user.groups.get().name
    role_id = get_role_id(role_name) if role_name else None

    if check_role(request, ROLE_FAMILY_SUPER_USER) and ((role_id == ROLE_FAMILY_SUPER_USER and request.user.id != long(id))
                                              or user.is_superuser):
        return False
    if check_role(request, ROLE_MEMBER) and ((role_id == ROLE_MEMBER and request.user.id != long(id))
                                         or role_id not in (ROLE_FAMILY_COMMON_USER, ROLE_FAMILY_SUPER_USER)):
        return False
    if check_role(request, ROLE_FAMILY_COMMON_USER) and user.username != request.user.username:
        return False
    return True


# 只有家庭管理员和系统管理员才有查看和修改普通成员的信息的权限
def check_permission(request, id):
    # 根据id获取用户
    # user_id = int(id)
    # user = get_object_or_404(User, id=user_id)
    #
    # # 获取用户角色名:
    # role_name = None
    # if user.groups.count() > 0:
    #     role_name = user.groups.get().name
    #
    # # 获取用户所对应的id
    # role_id = get_role_id(role_name) if role_name else None
    #
    # # 判断用户权限是否符合
    # if check_role(request, ROLE_SYSADMIN) and (user.is_superuser or )

    pass
