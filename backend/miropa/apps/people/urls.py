# coding=utf-8
from django.conf.urls import patterns, url

from apps.people import views


urlpatterns = patterns(
    '',
    url(r'^register/$', views.register_user),
    url(r'^categories/get', views.get_categories),
    # url(r'^materials/get', views.get_materials),
    # url(r'^tags/get', views.get_tags),
    # url(r'^posts/get', views.get_posts),
)
