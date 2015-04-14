#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

from django.shortcuts import render, redirect

from user_account.models import UserLoginForm
from django.contrib.auth import authenticate, login, logout


#  返回之前的现场
def back_to_original_page(request, url = "/"):
    if request.POST.has_key('redirect_url') and request.POST['redirect_url']:
        return redirect(request.POST['redirect_url'])
    else:
        return redirect(url)


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
        if cleaned_data.has_key('needRemember') and cleaned_data['needRemember']:
            request.session.set_expiry(2678400)  # session保持一个月

        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return back_to_original_page(request, "/")

    return render(request, "user_account/login.html", {
        "form": form,
        "app_version": settings.APP_VERSION,
    })


def logout_action(request):
    """
    注销动作
    """
    logout(request)
    return redirect(settings.LOGIN_URL)