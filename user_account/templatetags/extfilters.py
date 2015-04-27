# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, datetime

from django import template
from django.db import connection
from django.template.defaulttags import register
from django.utils.encoding import force_unicode
from django.conf import settings


register = template.Library()

@register.filter(name='in_group')
def in_group(user, groups):
    """Returns a boolean if the epiao_account is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if epiao_account|in_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if epiao_account|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    group_list = force_unicode(groups).split(',')
    return bool(user.groups.filter(name__in=group_list).values('name'))


@register.filter(name='format_date')
def format_date(value):
    if isinstance(value, date):
        return value.strftime(settings.DATE_INPUT_FORMATS[1])
    else:
        return value


@register.filter(name='format_datetime')
def format_datetime(value):
    if isinstance(value, datetime):
        return value.strftime(settings.DATETIME_INPUT_FORMATS[1])
    else:
        return value