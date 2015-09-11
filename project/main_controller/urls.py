from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'main_controller.views.index'),
    url(r'^howitworks/$', 'main_controller.views.howitworks')
)    