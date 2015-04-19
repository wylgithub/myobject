#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from captcha.fields import CaptchaField
from django import forms
from django.contrib.admindocs.utils import ROLES
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.forms import Form, ModelForm
import re
from utility.role_manager import ROLE_FAMILY_COMMON_USER


class MyUserManage(UserManager):
    # 创建user
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, is_active=True, is_superuser=False,
                          last_login=datetime.datetime.now(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 创建超级管理员
    def create_superuser(self, username, password, **extra_fields):
        u = self.create_user(username, password, **extra_fields)
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(PermissionsMixin):
    username = models.CharField(_("username"), max_length=40, db_index=True, unique=True)
    create_datetime = models.DateTimeField(auto_now_add=True)  # 用户的创建日期
    update_datetime = models.DateTimeField(auto_now=True)  # 用户的更新日期
    mobile = models.CharField(u"手机号码", max_length=15)  # 手机号码
    email = models.EmailField(u"邮箱", max_length=50)  # 邮箱
    full_name = models.CharField(_("full_name"), max_length=20)  # 用户的全名
    password = models.CharField(_("password"), max_length=128)  # 用户的密码
    last_login = models.DateTimeField(_('date joined'), default=datetime.datetime.now())  # 用户上一次登录的日期时间。默认设置为当前的日期和时间。
    is_active = models.BooleanField(default=True)  # 标识用户能否登录到admin界面。如果不想删除用户请把它设为 False
    objects = MyUserManage()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def get_username(self):
        """
        Return the identifying username for this User
        :return:
        """
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return self.get_username(),

    def is_anonymous(self):
        """
        总是返回 False 。这是区别 User and AnonymousUser 对象的一个方法。通常你应该使用 is_authenticated() 而不是这个方法。
        """
        return False

    def is_authenticated(self):
        """
        总是返回 True 。这是测试用户是否被认证了。.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password", "update_datetime"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_short_name(self):
        raise self.get_full_name()

    def get_full_name(self):
        return self.full_name if self.full_name else self.username

    def has_role(self, role):
        return role in ROLES and self.groups.filter(name=ROLES[role]).exists()

    class Meta:
        permissions = (
            ("view_user", u"能否查看用户"),
        )
        db_table = "graduation_design_account_user"  # 这里没有弄明白使用db_table为什么会报错，而使用app_label不会报错,这个问题在家里行不通，可视在公司测试了一下居然行了
        # app_label = 'user_account'

    def __unicode__(self):
        return self.username


class UserForm(ModelForm):
    role = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name', 'email', 'mobile')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        #  检查用户的唯一性
        if 'username' in cleaned_data and 'mode' in cleaned_data:
            username = cleaned_data['username']
            if User.objects.filter(username=username).count() > 0:
                msg = u"用户名已存在。"
                self._errors["username"] = self.error_class([msg])

                del cleaned_data["username"]

        if 'password' in cleaned_data:
            password = cleaned_data['password']
            if len(password) < 6:
                msg = u"为了您的账户安全，请您将密码位数设置的复杂点，尽量不要讲生日设置为个人密码！"
                self._errors['password'] = self.error_class([msg])

                del cleaned_data["password"]

        if 'mobile' in cleaned_data:
            mobile = cleaned_data['mobile']
            if mobile.isdigit():
                if len(mobile) != 11:
                    msg = u"请输入正确的手机号码！例如：15925087562"
                    self._errors['mobile'] = self.error_class([msg])

                    del cleaned_data['mobile']

        # 用户注册邮箱验证试用Django的认证方式
        # if 'email' in cleaned_data:
        #     email = cleaned_data['email']
        #     if len(email) > 7:
        #         if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
        #             msg = u"请输入正确的邮箱地址,例如：xxxxxx@163.com"
        #             self._errors = self.error_class([msg])
        #
        #             del cleaned_data['email']

        return cleaned_data


class UserRegisterForm(ModelForm):
    role = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name', 'email', 'mobile')

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        #  检查用户的唯一性
        if 'username' in cleaned_data and 'mode' in cleaned_data:
            username = cleaned_data['username']
            if User.objects.filter(username=username).count() > 0:
                msg = u"用户名已存在。"
                self._errors["username"] = self.error_class([msg])

                del cleaned_data["username"]

        if 'password' in cleaned_data:
            password = cleaned_data['password']
            if len(password) < 6:
                msg = u"为了您的账户安全，请您将密码位数设置的复杂点，尽量不要讲生日设置为个人密码！"
                self._errors['password'] = self.error_class([msg])

                del cleaned_data["password"]

        if 'mobile' in cleaned_data:
            mobile = cleaned_data['mobile']
            if mobile.isdigit():
                if len(mobile) != 11:
                    msg = u"请输入正确的手机号码！例如：15925087562"
                    self._errors['mobile'] = self.error_class([msg])

                    del cleaned_data['mobile']

        # 用户注册邮箱验证试用Django的认证方式
        # if 'email' in cleaned_data:
        #     email = cleaned_data['email']
        #     if len(email) > 7:
        #         if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
        #             msg = u"请输入正确的邮箱地址,例如：xxxxxx@163.com"
        #             self._errors = self.error_class([msg])
        #
        #             del cleaned_data['email']

        return cleaned_data


class UserEditForm(UserForm):

    class Meta:
        model = User
        fields = ('username', 'full_name')


class UserLoginForm(Form):
    username = forms.CharField(required=True, max_length=30)
    password = forms.CharField(required=True, max_length=20)
    needRemember = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()

        if 'username' in cleaned_data and cleaned_data. has_key('password'):
            username = cleaned_data['username']
            password = cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    msg = u"该用户已禁用。"
                    self._errors["username"] = self.error_class([msg])
                    del cleaned_data["username"]
            else:
                msg = u"用户不存在或者密码不正确。"
                self._errors["password"] = self.error_class([msg])

                del cleaned_data["password"]

        return cleaned_data