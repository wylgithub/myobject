#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wyl'


# 家庭收入类型
INCOME_TYPE_FOR_WORK = 10  # 工作收入
INCOME_TYPE_FOR_INVEST = 20  # 投资收入
INCOME_TYPE_FOR_OTHER = 30  # 投资收入
INCOME_TYPE_CHOICE = (
    (INCOME_TYPE_FOR_WORK, U'工作收入'),
    (INCOME_TYPE_FOR_INVEST, U'投资收入'),
    (INCOME_TYPE_FOR_OTHER, U'其它收入'),
)
INCOME_TYPE_DICT = dict((x, y) for x, y in INCOME_TYPE_CHOICE)


# 系统中使用的格式化日期配置
DATE_INPUT_FORMATS = ('%Y/%m/%d',)
DATE_TIME_FORMATS = ('%Y-%m-%d %H:%M',)
DATE_INPUT_FORMAT_SLASH = '%Y/%m/%d'
DATE_INPUT_FORMAT_HYPHEN = '%Y-%m-%d'
DATE_INPUT_FORMAT_HYPHEN_DETAIL = '%Y-%m-%d %H:%M'

# 与前台Ajax互动返回的各种错误代码
JSON_ERROR_CODE_NO_ERROR = 0  # 没有错误