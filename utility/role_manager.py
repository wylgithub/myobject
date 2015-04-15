#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group

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
