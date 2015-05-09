from django.conf.urls import patterns, include, url


from django.contrib import admin
from myobject.views import index_view

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^$', index_view),

    url(r'^user_account/', include('user_account.urls')),
    url(r'^income/', include('income.urls')),
    url(r'^plan/', include('plan.urls')),
    url(r'^stock/', include('stock.urls')),
    url(r'^get_total/', include('get_total.urls')),
)
