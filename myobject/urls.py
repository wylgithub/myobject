from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from myobject.views import get_current_datetime

admin.autodiscover()

urlpatterns = patterns('',
    (r'^show_time/$', get_current_datetime),
)
