#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def add_income_view(request):
    """
    添加收入明细view
    :param request:
    :return:
    """
    return render(request, "income/add_income.html", {

    })


@login_required
def income_list_view(request):
    """
    收入明细一览表
    :param request:
    :return:
    """

    return render(request, "income/income_detail.html", {

    })
