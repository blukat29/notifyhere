from django.conf.urls import patterns, url

from dash import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^auth/(?P<service>[a-zA-Z]+)/$', views.auth, name='auth'),
    url(r'^ajax/(?P<service>[a-zA-Z]+)/$', views.ajax, name='ajax'),
)
