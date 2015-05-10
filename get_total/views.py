#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from income.models import Income, Expend, Borrow, Lend
from utility.base_view import get_list_params


@login_required
def get_total_list_view(request):

    # 收入信息接受对象
    income_list = []
    total_income = 0

    # 支出信息接受对象
    expend_list = []
    total_expend = 0

    # 借入信息接受对象
    borrow_list = []
    total_borrow = 0

    # 借出信息接受对象
    lend_list = []
    total_lend = 0

    # 获取家庭收入信息汇总
    income_queryset = Income.objects.filter(delete_flg=False)

    # 获取收入金额存于列表
    for income in income_queryset:
        income_list.append(int(income.income_amount))
    # 获取总收入
    for amount in income_list:
        total_income += amount

    # 获取家庭之处信息汇总
    expend_queryset = Expend.objects.filter(delete_flg=False)

    for expend in expend_queryset:
        expend_list.append(int(expend.expend_amount))

    for amount in expend_list:
        total_expend += amount

    # 获取家庭借入信息汇总
    borrow_queryset = Borrow.objects.filter(delete_flg=False)

    for borrow in borrow_queryset:
        borrow_list.append(int(borrow.borrow_amount))

    for amount in borrow_list:
        total_borrow += amount

    # 获取家庭借出信息汇总
    lend_queryset = Lend.objects.filter(delete_flg=False)

    for lend in lend_queryset:
        lend_list.append(int(lend.lend_amount))

    for amount in lend_list:
        total_lend += amount

    return render(request, "get_total/get_total_list.html", {
        "total_income": total_income,
        "total_expend": total_expend,
        "total_borrow": total_borrow,
        "total_lend": total_lend,
    })


@login_required
def get_income_collect(request):
    """
    对家庭收入信息进行选择时间段汇总
    :param request:
    :return:
    """
    # 收入信息接受对象
    income_list = []
    total_income = 0

    time_is_ok, error_message = False, None  # 初始化参数。
    # 从地址栏取得时间段，没有的不查询。
    if 'sss' in request.GET and 'eee' in request.GET:
        try:
            start_time = datetime.strptime(request.GET['sss'], "%Y-%m-%d")
            end_time = datetime.strptime(request.GET['eee'], "%Y-%m-%d")+timedelta(days=1)
            assert(start_time < end_time)
            time_is_ok = True
        except ValueError:
            error_message = u"时间参数错误，请联系管理员"
        except AssertionError:
            error_message = u"结束时间不得大于开始时间，请修改后重新结算"
    if time_is_ok:
        order_dict = {
            u"ty": "income_type",
            u"am": "income_amount",
            u"tm": "create_datetime",
            u"hl": "handler",
            u"mk": "remarks",
        }
        queryset = Income.objects.filter(
            delete_flg=False,
            create_datetime__gte=start_time,
            create_datetime__lt=end_time
        )
        for income in queryset:
            income_list.append(int(income.income_amount))
        # 获取总收入
        for amount in income_list:
            total_income += amount
        # 取得画面列表参数
        params = get_list_params(request)
        # 添加起始时段画面参数。
        params['sss'] = request.GET['sss']
        params['eee'] = request.GET['eee']

        # 排序
        if not params['order_field'] or not params['order_field'] in order_dict:
            # 默认没有设定排序状态时，按照状态排序的默认方式进行排序
            queryset = queryset.order_by("create_datetime")
            params['order_field'] = "tm"
        else:
            queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))

        total_count = queryset.count()

        return render(request, "get_total/get_total_income.html", {
            "time_is_ok": time_is_ok,
            # "sum_dict": sum_dict,
            "time_content": u"从 %s 到 %s 的汇总：" % (start_time, end_time-timedelta(seconds=1)),
            "incomes": queryset[params['from']:params['to']],
            "query_params": params,
            "need_pagination": params['limit'] < total_count,
            "total_count": total_count,
            "sss_time_str": params['sss'],
            "eee_time_str": params['eee'],
            "total_income": total_income,
        })
    else:
        # 设置默认的检索时段。（上月初到月末）
        last_time = date.today().replace(day=1)-timedelta(days=1)
        sss_time_str = (last_time.replace(day=1)).strftime('%Y-%m-%d')
        eee_time_str = last_time.strftime('%Y-%m-%d')
        return render(request, "get_total/get_total_income.html", {
            "time_is_ok": time_is_ok,  # 无参数时提示的标志。
            "error_message": error_message,
            "total_count": 0,
            "sss_time_str": sss_time_str,
            "eee_time_str": eee_time_str,
        })


@login_required
def get_expend_collect(request):
    """
    对家庭收入信息进行选择时间段汇总
    :param request:
    :return:
    """
    # 收入信息接受对象
    expend_list = []
    total_expend = 0

    time_is_ok, error_message = False, None  # 初始化参数。
    # 从地址栏取得时间段，没有的不查询。
    if 'sss' in request.GET and 'eee' in request.GET:
        try:
            start_time = datetime.strptime(request.GET['sss'], "%Y-%m-%d")
            end_time = datetime.strptime(request.GET['eee'], "%Y-%m-%d")+timedelta(days=1)
            assert(start_time < end_time)
            time_is_ok = True
        except ValueError:
            error_message = u"时间参数错误，请联系管理员"
        except AssertionError:
            error_message = u"结束时间不得大于开始时间，请修改后重新结算"
    if time_is_ok:
        order_dict = {
            u"type": "expend_type",
            u"acc": "expend_account",
            u"amo": "expend_amount",
            u"bal": "balance",
            u"dat": "create_datetime",
            u"hl": "handler",
            u"mk": "remarks",
        }
        queryset = Expend.objects.filter(
            delete_flg=False,
            create_datetime__gte=start_time,
            create_datetime__lt=end_time
        )
        for expend in queryset:
            expend_list.append(int(expend.expend_amount))

        for amount in expend_list:
            total_expend += amount
        # 取得画面列表参数
        params = get_list_params(request)
        # 添加起始时段画面参数。
        params['sss'] = request.GET['sss']
        params['eee'] = request.GET['eee']

        # 排序
        if not params['order_field'] or not params['order_field'] in order_dict:
            # 默认没有设定排序状态时，按照状态排序的默认方式进行排序
            queryset = queryset.order_by("create_datetime")
            params['order_field'] = "tm"
        else:
            queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))

        total_count = queryset.count()

        return render(request, "get_total/get_total_expend.html", {
            "time_is_ok": time_is_ok,
            "time_content": u"从 %s 到 %s 的汇总：" % (start_time, end_time-timedelta(seconds=1)),
            "expends": queryset[params['from']:params['to']],
            "query_params": params,
            "need_pagination": params['limit'] < total_count,
            "total_count": total_count,
            "sss_time_str": params['sss'],
            "eee_time_str": params['eee'],
            "total_expend": total_expend,
        })
    else:
        # 设置默认的检索时段。（上月初到月末）
        last_time = date.today().replace(day=1)-timedelta(days=1)
        sss_time_str = (last_time.replace(day=1)).strftime('%Y-%m-%d')
        eee_time_str = last_time.strftime('%Y-%m-%d')
        return render(request, "get_total/get_total_expend.html", {
            "time_is_ok": time_is_ok,  # 无参数时提示的标志。
            "error_message": error_message,
            "total_count": 0,
            "sss_time_str": sss_time_str,
            "eee_time_str": eee_time_str,
        })


@login_required
def get_borrow_collect(request):
    """
    对家庭收入信息进行选择时间段汇总
    :param request:
    :return:
    """
    # 借入信息接受对象
    borrow_list = []
    total_borrow = 0

    time_is_ok, error_message = False, None  # 初始化参数。
    # 从地址栏取得时间段，没有的不查询。
    if 'sss' in request.GET and 'eee' in request.GET:
        try:
            start_time = datetime.strptime(request.GET['sss'], "%Y-%m-%d")
            end_time = datetime.strptime(request.GET['eee'], "%Y-%m-%d")+timedelta(days=1)
            assert(start_time < end_time)
            time_is_ok = True
        except ValueError:
            error_message = u"时间参数错误，请联系管理员"
        except AssertionError:
            error_message = u"结束时间不得大于开始时间，请修改后重新结算"
    if time_is_ok:
        order_dict = {
            u"type": "expend_type",
            u"acc": "expend_account",
            u"amo": "expend_amount",
            u"bal": "balance",
            u"dat": "create_datetime",
            u"hl": "handler",
            u"mk": "remarks",
        }
        queryset = Borrow.objects.filter(
            delete_flg=False,
            update_datetime__gte=start_time,
            update_datetime__lt=end_time
        )
        for borrow in queryset:
            borrow_list.append(int(borrow.borrow_amount))

        for amount in borrow_list:
            total_borrow += amount
        # 取得画面列表参数
        params = get_list_params(request)
        # 添加起始时段画面参数。
        params['sss'] = request.GET['sss']
        params['eee'] = request.GET['eee']

        # 排序
        if not params['order_field'] or not params['order_field'] in order_dict:
            # 默认没有设定排序状态时，按照状态排序的默认方式进行排序
            queryset = queryset.order_by("borrow_datetime")
            params['order_field'] = "dat"
        else:
            queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))

        total_count = queryset.count()

        return render(request, "get_total/get_total_borrow.html", {
            "time_is_ok": time_is_ok,
            "time_content": u"从 %s 到 %s 的汇总：" % (start_time, end_time-timedelta(seconds=1)),
            "borrows": queryset[params['from']:params['to']],
            "query_params": params,
            "need_pagination": params['limit'] < total_count,
            "total_count": total_count,
            "sss_time_str": params['sss'],
            "eee_time_str": params['eee'],
            "total_borrow": total_borrow,
        })
    else:
        # 设置默认的检索时段。（上月初到月末）
        last_time = date.today().replace(day=1)-timedelta(days=1)
        sss_time_str = (last_time.replace(day=1)).strftime('%Y-%m-%d')
        eee_time_str = last_time.strftime('%Y-%m-%d')
        return render(request, "get_total/get_total_borrow.html", {
            "time_is_ok": time_is_ok,  # 无参数时提示的标志。
            "error_message": error_message,
            "total_count": 0,
            "sss_time_str": sss_time_str,
            "eee_time_str": eee_time_str,
        })

@login_required
def get_lend_collect(request):
    """
    对家庭收入信息进行选择时间段汇总
    :param request:
    :return:
    """
    # 借入信息接受对象
    lend_list = []
    total_lend = 0

    time_is_ok, error_message = False, None  # 初始化参数。
    # 从地址栏取得时间段，没有的不查询。
    if 'sss' in request.GET and 'eee' in request.GET:
        try:
            start_time = datetime.strptime(request.GET['sss'], "%Y-%m-%d")
            end_time = datetime.strptime(request.GET['eee'], "%Y-%m-%d")+timedelta(days=1)
            assert(start_time < end_time)
            time_is_ok = True
        except ValueError:
            error_message = u"时间参数错误，请联系管理员"
        except AssertionError:
            error_message = u"结束时间不得大于开始时间，请修改后重新结算"
    if time_is_ok:
        order_dict = {
            u"op": "handler",
            u"jr": "lend_person",
            u"jc": "borrow_person",
            u"jj": "lend_amount",
            u"ky": "balance",
            u"jq": "lend_datetime",
            u"hq": "pay_datetime",
            u"mk": "remarks",
        }
        queryset = Lend.objects.filter(
            delete_flg=False,
            update_datetime__gte=start_time,
            update_datetime__lt=end_time
        )
        for lend in queryset:
            lend_list.append(int(lend.lend_amount))

        for amount in lend_list:
            total_lend += amount
        # 取得画面列表参数
        params = get_list_params(request)
        # 添加起始时段画面参数。
        params['sss'] = request.GET['sss']
        params['eee'] = request.GET['eee']

        # 排序
        if not params['order_field'] or not params['order_field'] in order_dict:
            # 默认没有设定排序状态时，按照状态排序的默认方式进行排序
            queryset = queryset.order_by("lend_datetime")
            params['order_field'] = "jq"
        else:
            queryset = queryset.order_by("%s%s" % (params['order_direction'], order_dict[params['order_field']]))

        total_count = queryset.count()

        return render(request, "get_total/get_total_lend.html", {
            "time_is_ok": time_is_ok,
            "time_content": u"从 %s 到 %s 的汇总：" % (start_time, end_time-timedelta(seconds=1)),
            "lends": queryset[params['from']:params['to']],
            "query_params": params,
            "need_pagination": params['limit'] < total_count,
            "total_count": total_count,
            "sss_time_str": params['sss'],
            "eee_time_str": params['eee'],
            "total_lend": total_lend,
        })
    else:
        # 设置默认的检索时段。（上月初到月末）
        last_time = date.today().replace(day=1)-timedelta(days=1)
        sss_time_str = (last_time.replace(day=1)).strftime('%Y-%m-%d')
        eee_time_str = last_time.strftime('%Y-%m-%d')
        return render(request, "get_total/get_total_lend.html", {
            "time_is_ok": time_is_ok,  # 无参数时提示的标志。
            "error_message": error_message,
            "total_count": 0,
            "sss_time_str": sss_time_str,
            "eee_time_str": eee_time_str,
        })