# !/usr/bin/env python
# -*- coding: utf-8 -*-

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
