# This file is part discount_base_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    @fields.depends('base_price', methods=['on_change_discount_rate'])
    def on_change_base_price(self):
        if self.base_price is not None:
            if self.discount_rate is not None:
                self.on_change_discount_rate()
            else:
                self.unit_price = self.base_price
