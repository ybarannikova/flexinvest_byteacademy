from django.conf.urls import patterns, include, url
from users.admin import admin_site

urlpatterns = patterns('',
    url(r'^', include('main_controller.urls')),
    url(r'^admin/', include(admin_site.urls)),
    url(r'^', include('users.urls')),
    url(r'^flex/', include('flex.urls', namespace='flex', app_name='flex')),
    url(r'^cashflow/', include('cashflow.urls')),
)
