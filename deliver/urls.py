__author__ = 'alya'
from django.conf.urls import patterns, url
from deliver import views

urlpatterns = patterns('',

  url(r'^add_address/$', views.add_address, name='add_address'),





)

