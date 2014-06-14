#!/usr/bin/python
# -*- coding: utf-8 -*-


from django import forms
from django.contrib.auth.models import User
from deliver.models import dAddress
from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _, pgettext_lazy


class dAddressForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text=u"Имя")
    last_name=forms.CharField(max_length=128,help_text=u"Фамилия")
    phone =forms.CharField(max_length=20, help_text=u"Телефон")
    address=forms.CharField(max_length=450, help_text=u"Адресс")

    message = forms.CharField(widget=forms.Textarea(attrs={ 'rows': 5}), max_length=500, help_text=u" Дополнительная информация")



    class Meta:
        # Provide an association between the ModelForm and a model
        model = dAddress