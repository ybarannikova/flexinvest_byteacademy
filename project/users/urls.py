from django.conf.urls import include, url, patterns
from django.contrib import admin
from users.views import Login, Register, Logout

urlpatterns = patterns('users.views',
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
)
