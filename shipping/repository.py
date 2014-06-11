from decimal import Decimal as D

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from oscar.apps.shipping.repository import Repository as BaseRepository

from shipping import methods
from decimal import Decimal as D

class Repository(BaseRepository):
    def get_shipping_methods(self, user, basket, shipping_addr=None,
                             request=None, **kwargs):
        if not basket.is_shipping_required():
            return [methods.NoShippingRequired()]

        methods_ = [methods.NoShippingRequired()]
        if shipping_addr:
            if shipping_addr.city == u'Пермь':
                methods_ = [InnerPerm(
                    basket.num_items, Decimal('10000'), Decimal('11000')
                )]
            else:
                methods_ = [OutterPerm(
                    basket.num_items, Decimal('20000'), Decimal('22000')
                )]
        return self.prime_methods(basket, methods_)