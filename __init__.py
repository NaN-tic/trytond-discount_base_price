# This file is part discount_base_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

def register():
    Pool.register(
        module='discount_base_price', type_='model')
    Pool.register(
        module='discount_base_price', type_='wizard')
    Pool.register(
        module='discount_base_price', type_='report')
