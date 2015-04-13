#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login

from django.shortcuts import render_to_response, render

# Create your views here.
from user_account.models import UserLoginForm


def login_view(request):
    """
    登录view
    """
    return render_to_response("user_account/login.html")


def login_action(request):
    """
    登录动作
    :param request:
    :return:
    """
    form = UserLoginForm(request.POST)

    if form.is_valid():
        cleaned_data = form.clead_data
        if cleaned_data.has_key('needRemember') and cleaned_data['needRemember']:
            request.session.set_expiry(2678400)  # session保持一个月

        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)