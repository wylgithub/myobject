#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import datetime


__author__ = 'xieyibin'


def get_today():
    """取得当前日期"""
    return datetime.date.today()


def get_now():
    """取得当前日时"""
    return datetime.datetime.now()


def add_days(days=0, base=datetime.date.today()):
    """
    一个日期加上给定天数
    :param base 基础日期
    :param days 天数
    """
    return base + datetime.timedelta(days=days)


def sub_days(days=0, base=datetime.date.today()):
    """
    一个日期减去给定天数
    :param base 基础日期
    :param days 天数
    """
    return base - datetime.timedelta(days=days)


def add_months(months=0, base=datetime.date.today()):
    """
    一个日期加上给定月数
    :param base 基础日期
    :param months 月数
    """
    month = base.month - 1 + months
    year = base.year + month / 12
    month = month % 12 + 1
    day = min(base.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

# def add_months(months=0, base=datetime.date.today()):
#     """
#     一个日期加上给定月数
#     :param base 基础日期
#     :param months 月数
#     """
#     month = base.month + months
#
#     year = base.year
#     if month > 0:
#         # >12个月才需要+1年
#         year += (month - 1) / 12
#     else:
#         # 正好0，那就是前一年的12月份
#         if month == 0:
#             year -= 1
#         else:
#             year -= ((-month) / 12 + 1)
#
#
#     if month <= 0:
#         month = 12 - ((-month) % 12)
#     else:
#         month %= 12
#
#     # 正好12个月，则定位12月份
#     if month == 0:
#         month = 12
#     day = min(base.day, calendar.monthrange(year, month)[1])
#
#     return datetime.date(year, month, day)


def sub_months(months=0, base=datetime.date.today()):
    """
    一个日期减去给月数
    :param base 基础日期
    :param months 月数
    """
    return add_months(-months, base)


def is_gte_today(base):
    """
    判断给定日期是否大于等于当前日期
    :param base 基础日期
    """
    return True if base >= datetime.date.today() else False


def is_lte_today(base):
    """
    判断给定日期是否小于当前日期
    :param base 基础日期
    """
    return True if base < datetime.date.today() else False


def is_valid_date(str_base):
    """
    判断给定日期字符串是否为有效日期
    :param str_base 基础日期字符串
    """
    try:
        datetime.datetime.strptime(str_base, '%Y/%m/%d')
    except ValueError:
        return False
    return True


def to_date(str_base, type='%Y/%m/%d'):
    """
    将给定日期字符串转换为日期
    :param str_base 基础日期字符串
    """
    base_datetime = datetime.strptime(str_base, type)
    return base_datetime.date()


def to_datetime(str_base, type='%Y-%m-%d %H:%M'):
    """
    将给定日期字符串转换为日时
    :param str_base 基础日时字符串
    """
    base_datetime = datetime.datetime.strptime(str_base, type)
    return base_datetime