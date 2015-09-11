from django.conf.urls import patterns, include, url
from .views import Index, Investing, Portfolio, Account, Investments, InvestingApi, Contract, Activity, Purchase, TrancheurView


urlpatterns = patterns('',

    url(r'^$', Index.as_view()),
    url(r'^investing/$', Investing.as_view()),
    url(r'^portfolio/$', Portfolio.as_view()),
    url(r'^portfolio/investments', Investments.as_view()),
    url(r'^portfolio/activity', Activity.as_view()),
    url(r'^portfolio/contract', Contract.as_view()),
    url(r'^account/$', Account.as_view()),
    url(r'^purchase/$', Purchase.as_view()),
    url(r'^api/investing/', InvestingApi.as_view()),
    url(r'^trancheur/$', TrancheurView.as_view()),

)
