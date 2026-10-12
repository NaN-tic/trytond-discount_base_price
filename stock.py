# This file is part discount_base_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'

    @fields.depends('base_price', methods=['on_change_discount_rate'])
    def on_change_base_price(self):
        if self.base_price is not None:
            if self.discount_rate is not None:
                self.on_change_discount_rate()
            else:
                self.unit_price = self.base_price
