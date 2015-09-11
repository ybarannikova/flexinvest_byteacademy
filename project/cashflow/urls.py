from django.conf.urls import include, url, patterns
from django.contrib import admin
from cashflow.views import UserCashflows

urlpatterns = patterns('',
    url(r'^user_cashflows/', UserCashflows.as_view(), name = 'user_cashflows'),
)
