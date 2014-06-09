__author__ = 'alya'

from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^pay/$', 'pay.views.pay', name='pay'),

)