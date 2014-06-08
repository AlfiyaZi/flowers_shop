from django import forms
from django.contrib.auth.models import User
from contact.models import Contact
class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    phone = forms.CharField(max_length=15)
    message = forms.CharField(max_length=250)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Contact