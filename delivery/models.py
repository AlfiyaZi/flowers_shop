import re
import zlib

from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from django.core import exceptions
from oscar.core.compat import AUTH_USER_MODEL
from oscar.models.fields import UppercaseCharField


class CustomerAddress(models.Model):


    first_name = models.CharField( max_length=255, blank=True, help_text=u"Имя")
    last_name = models.CharField(max_length=255, blank=True,  help_text=u"Фамилия")


    line1 = models.CharField(_("First line of deliver"), max_length=255)
    line2 = models.CharField(
        _("Second line of deliver"), max_length=255, blank=True)

    search_text = models.CharField(
        _("Search text - used only for searching addresses"),
        max_length=1000, editable=False)




    def __unicode__(self):
        return self.summary

    class Meta:

        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    # Saving

    def save(self, *args, **kwargs):
        self._update_search_text()
        super(CustomerAddress, self).save(*args, **kwargs)

    def clean(self):
        # Strip all whitespace
        for field in ['first_name', 'last_name', 'line1', 'line2']:
            if self.__dict__[field]:
                self.__dict__[field] = self.__dict__[field].strip()





    def _update_search_text(self):
        search_fields = filter(
            bool, [self.first_name, self.last_name,
                   self.line1, self.line2
                   ])
        self.search_text = ' '.join(search_fields)

    # Properties

    @property
    def city(self):
        # Common alias
        return self.line4

    @property
    def summary(self):
        """
        Returns a single string summary of the deliver,
        separating fields using commas.
        """
        return u", ".join(self.active_address_fields())

    @property
    def salutation(self):
        """
        Name (including title)
        """
        return self.join_fields(
            ('first_name', 'last_name'),
            separator=u" ")

    @property
    def name(self):
        return self.join_fields(('first_name', 'last_name'), separator=u" ")

    # Helpers

    def generate_hash(self):
        """
        Returns a hash of the deliver summary
        """
        # We use an upper-case version of the summary
        return zlib.crc32(self.summary.strip().upper().encode('UTF8'))

    def join_fields(self, fields, separator=u", "):
        """
        Join a sequence of fields using the specified separator
        """
        field_values = []
        for field in fields:
            value = getattr(self, field)
            field_values.append(value)
        return separator.join(filter(bool, field_values))

    def populate_alternative_model(self, address_model):
        """
        For populating an deliver model using the matching fields
        from this one.

        This is used to convert a user deliver to a shipping deliver
        as part of the checkout process.
        """
        destination_field_names = [
            field.name for field in address_model._meta.fields]
        for field_name in [field.name for field in self._meta.fields]:
            if field_name in destination_field_names and field_name != 'id':
                setattr(address_model, field_name, getattr(self, field_name))

    def active_address_fields(self, include_salutation=True):
        """
        Return the non-empty components of the deliver, but merging the
        title, first_name and last_name into a single line.
        """
        fields = [self.line1, self.line2]
        if include_salutation:
            fields = [self.salutation] + fields
        fields = [f.strip() for f in fields if f]
        return fields




class CShippingAddress(CustomerAddress):
    """
    A shipping deliver.

    A shipping deliver should not be edited once the order has been placed -
    it should be read-only after that.
    """
    phone_number = models.CharField( _("Phone number"), blank=True, max_length=30,
        help_text=_("In case we need to call you about your order"))
    notes = models.TextField(
        blank=True, verbose_name=_('Instructions'),
        help_text=_("Tell us anything we should know when delivering "
                    "your order."))

    class Meta:

        verbose_name = _("Shipping deliver")
        verbose_name_plural = _("Shipping addresses")

    @property
    def order(self):
        """
        Return the order linked to this shipping deliver
        """
        try:
            return self.order_set.all()[0]
        except IndexError:
            return None


class AUserAddress(CShippingAddress):
    """
    A user's deliver.  A user can have many of these and together they form an
    'deliver book' of sorts for the user.

    We use a separate model for shipping and billing (even though there will be
    some data duplication) because we don't want shipping/billing addresses
    changed or deleted once an order has been placed.  By having a separate
    model, we allow users the ability to add/edit/delete from their deliver
    book without affecting orders already placed.
    """
    user = models.ForeignKey(
        AUTH_USER_MODEL, related_name='addresses', verbose_name=_("User"))

    #: Whether this deliver is the default for shipping
    is_default_for_shipping = models.BooleanField(
        _("Default shipping deliver?"), default=False)

    #: Whether this deliver should be the default for billing.
    is_default_for_billing = models.BooleanField(
        _("Default billing deliver?"), default=False)

    #: We keep track of the number of times an deliver has been used
    #: as a shipping deliver so we can show the most popular ones
    #: first at the checkout.
    num_orders = models.PositiveIntegerField(_("Number of Orders"), default=0)

    #: A hash is kept to try and avoid duplicate addresses being added
    #: to the deliver book.
    hash = models.CharField(_("Address Hash"), max_length=255, db_index=True,
                            editable=False)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Save a hash of the deliver fields
        """
        # Save a hash of the deliver fields so we can check whether two
        # addresses are the same to avoid saving duplicates
        self.hash = self.generate_hash()

        # Ensure that each user only has one default shipping deliver
        # and billing deliver
        self._ensure_defaults_integrity()
        super(AUserAddress, self).save(*args, **kwargs)

    def _ensure_defaults_integrity(self):
        if self.is_default_for_shipping:
            self.__class__._default_manager\
                .filter(user=self.user, is_default_for_shipping=True)\
                .update(is_default_for_shipping=False)
        if self.is_default_for_billing:
            self.__class__._default_manager\
                .filter(user=self.user, is_default_for_billing=True)\
                .update(is_default_for_billing=False)

    class Meta:

        verbose_name = _("User deliver")
        verbose_name_plural = _("User addresses")
        ordering = ['-num_orders']
        unique_together = ('user', 'hash')

    def validate_unique(self, exclude=None):
        super(CustomerAddress, self).validate_unique(exclude)
        qs = self.__class__.objects.filter(
            user=self.user,
            hash=self.generate_hash())
        if self.id:
            qs = qs.exclude(id=self.id)
        if qs.exists():
            raise exceptions.ValidationError({
                '__all__': [_("This deliver is already in your deliver"
                              " book")]})


class AbstractBillingAddress(CustomerAddress):

    class Meta:
        abstract = True
        verbose_name = _("Billing deliver")
        verbose_name_plural = _("Billing addresses")

    @property
    def order(self):
        """
        Return the order linked to this shipping deliver
        """
        try:
            return self.order_set.all()[0]
        except IndexError:
            return None


class AbstractPartnerAddress(CustomerAddress):
    """
    A partner can have one or more addresses. This can be useful e.g. when
    determining US tax which depends on the origin of the shipment.
    """
    partner = models.ForeignKey('partner.Partner', related_name='addresses',
                                verbose_name=_('Partner'))

    class Meta:
        abstract = True
        verbose_name = _("Partner deliver")
        verbose_name_plural = _("Partner addresses")
