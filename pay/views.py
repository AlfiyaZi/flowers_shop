#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from robokassa.forms import *


@login_required
def pay(request):
   # order = get_object_or_404(Order, pk=order_id)

    form = RobokassaForm(initial={
               #'orderId': 7,
               'OutSum': 100.00,
               'InvId': 58,
               'Desc' : u'Холодильник "Бирюса"',
               'Email': request.user.email,
                #'IncCurrLabel': '',
                #'Culture': 'ru'
           })

    return render(request, 'pay/pay.html', {'form': form})
