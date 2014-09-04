#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from robokassa.forms import *




from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from robokassa.forms import RobokassaForm





from oscar.apps.checkout import views
from oscar.apps.payment import models


class PaymentDetailsView(views.PaymentDetailsView):


    def handle_place_order_submission(self, request):
        from robokassa.forms import RobokassaForm

        #@login_required
        #def pay_with_robokassa(request):
        form = RobokassaForm(initial={
                   'OutSum': Decimal('10.00'),
                   'InvId':58,
                   'Desc' : u'Холодильник "Бирюса"',
                   'Email': request.user.email,
                   # 'IncCurrLabel': '',
                   # 'Culture': 'ru'
                                 })

        return render(request, 'pay/pay.html', {'form': form})


        """
        Handle a request to place an order.

        This method is normally called after the customer has clicked "place
        order" on the preview page. It's responsible for (re-)validating any
        form information then building the submission dict to pass to the
        `submit` method.

        If forms are submitted on your payment details view, you should
        override this method to ensure they are valid before extracting their
        data into the submission dict and passing it onto `submit`.
        """
        #return self.submit(**self.build_submission())




    def handle_payment_details_submission(self, request):
        """
        Handle a request to submit payment details.

        This method will need to be overridden by projects that require forms
        to be submitted on the payment details view.  The new version of this
        method should validate the submitted form data and:

        - If the form data is valid, show the preview view with the forms
          re-rendered in the page
        - If the form data is invalid, show the payment details view with
          the form errors showing.

        """
        # No form data to validate by default, so we simply render the preview
        # page.  If validating form data and it's invalid, then call the
        # render_payment_details view.
        return self.render_preview(request)




    def handle_payment(self, order_number, total, **kwargs):
        # Talk to payment gateway.  If unsuccessful/error, raise a
        # PaymentError exception which we allow to percolate up to be caught
        # and handled by the core PaymentDetailsView.









        source_type, __ = models.SourceType.objects.get_or_create(
            name="robokassa")
        source = models.Source(
            source_type=source_type,
            amount_allocated=total.incl_tax,
            )
        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('pre-auth', total.incl_tax)