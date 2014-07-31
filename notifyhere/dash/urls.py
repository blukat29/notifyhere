from django.conf.urls import patterns, url

from dash import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^auth/redirect/(?P<service>[a-zA-Z]+)/$', views.auth_redirect, name='auth_redirect'),
    url(r'^auth/callback/(?P<service>[a-zA-Z]+)/$', views.auth_callback, name='auth_callback'),
    url(r'^auth/logout/(?P<service>[a-zA-Z]+)/$', views.auth_logout, name='auth_logout'),
    url(r'^ajax/(?P<service>[a-zA-Z]+)/$', views.ajax, name='ajax'),
)
