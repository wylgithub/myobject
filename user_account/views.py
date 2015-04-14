#!/usr/bin/env python
# -*- coding: utf-8 -*-
import captcha
from captcha.models import CaptchaStore
from django.conf import settings

from django.shortcuts import render, redirect

from user_account.models import UserLoginForm, UserForm
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