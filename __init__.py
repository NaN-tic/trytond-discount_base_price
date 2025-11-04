# This file is part discount_base_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import invoice
from . import sale

def register():
    Pool.register(
        invoice.InvoiceLine,
        depends=['account_invoice_discount'],
        module='discount_base_price', type_='model')
    Pool.register(
        sale.SaleLine,
        depends=['sale_discount'],
        module='discount_base_price', type_='model')
