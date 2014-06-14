#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _, pgettext_lazy

class dAddress(models.Model):
    name = models.CharField(max_length=128, help_text=u"Имя", blank=True)
    last_name=models.CharField(max_length=128,help_text=u"Фамилия")
    phone = models.CharField(max_length=20, help_text=u"Телефон")
    address=models.CharField(max_length=450, help_text=u"Адресс")

    message = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name







