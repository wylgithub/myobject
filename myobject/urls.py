from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from myobject.views import get_current_datetime

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', get_current_datetime),

    url(r'^user_account/', include('user_account.urls')),
)
