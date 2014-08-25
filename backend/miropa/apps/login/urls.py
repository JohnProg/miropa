# coding=utf-8
from django.conf.urls import patterns, url

from apps.login import views


urlpatterns = patterns(
    '',
    url(r'^login/$', views.login_user),
    url(r'^logout/$', views.logout_user),
)
