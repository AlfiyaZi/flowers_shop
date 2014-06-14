from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from models import *


class CustomerAddressForm(forms.ModelForm):
    first_name = forms.CharField(_("First name"))
    last_name = forms.CharField(_("Last name"), max_length=255, blank=True)
    line1 = forms.CharField(_("First line of deliver"), max_length=255)
    line2 = forms.CharField( _("Second line of deliver"), max_length=255, blank=True)

    search_text = forms.CharField(
        _("Search text - used only for searching addresses"),
        max_length=1000, editable=False)
    class Meta:
        # Provide an association between the ModelForm and a model
        model =CustomerAddress



class AUserAddressForm(CustomerAddressForm):

    class Meta:
        model = AUserAddress
        exclude = ('user', 'num_orders', 'hash', 'search_text',
                   'is_default_for_billing', 'is_default_for_shipping')

    def __init__(self, user, *args, **kwargs):
        super(AUserAddressForm, self).__init__(*args, **kwargs)
        self.instance.user = user
