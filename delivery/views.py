#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from delivery.forms import *

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect
from forms import *


def add_address(request):
    # Get the context from the request.
    context = RequestContext(request)
    # A HTTP POST?
    if request.method == 'POST':
        form = AUserAddressForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.



            form.save(commit=True)



    else:
        # If the request was not a POST, display the form to enter details.
        form = AUserAddressForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).

    return render_to_response('deliver/add_address.html',  context)
