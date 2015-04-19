#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import re


__author__ = 'wyl'


def is_valid_phone_number(phone_number):
    return phone_number is not None and re.match(r'^((\d{3,4}-)?\d{7,8})$|(1[0-9]{10})$', str(phone_number))


def is_valid_zip_code(zip_code):
    return zip_code is not None and re.match(r'^[0-9]{6}$', str(zip_code))


def is_int(value):
    try:
        result = int(value)
        return True
    except:
        return False


def is_long(value):
    try:
        result = long(value)
        return True
    except:
        return False


def is_date(value):
    if value is None:
        return False

    result = None

    for format in ['%Y/%m/%d', ]:
      try:
        result = datetime.strptime(value, format)
      except:
        pass

    return result is not None