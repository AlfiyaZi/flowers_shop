from django.db import models
from django.contrib.auth.models import User
#!/usr/bin/python
# -*- coding: utf-8 -*-


class Contact(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    message = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name

