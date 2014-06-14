#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from delivery import views

urlpatterns = patterns('',

                       url(r'^add_address/$', views.add_address, name='add_address'),





)

