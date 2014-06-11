from decimal import Decimal as D
from django.template.loader import render_to_string


from django.utils.translation import ugettext_lazy as _

from oscar.apps.shipping.base import Base

from oscar.apps.shipping.methods import FixedPrice




class InnerPerm(FixedPrice):
    code='inner-perm'
    name =_('Inner Perm')

    def __init__(self, num_items, charge_excl_tax, charge_incl_tax=None):
        super(InnerPerm, self).__init__(charge_excl_tax, charge_incl_tax)
        self.charge_excl_tax = num_items * charge_excl_tax
        if charge_incl_tax is not None:
            self.charge_incl_tax = num_items * charge_incl_tax



class OuterPerm(FixedPrice):
    code='outer-perm'
    name =_('Outer Perm')

    def __init__(self, num_items, charge_excl_tax, charge_incl_tax=None):
        super(OuterPerm, self).__init__(charge_excl_tax, charge_incl_tax)
        self.charge_excl_tax = num_items * charge_excl_tax
        if charge_incl_tax is not None:
            self.charge_incl_tax = num_items * charge_incl_tax
