from decimal import Decimal
import unittest

from proteus import Model
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class TestStockBasePrice(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):
        activate_modules(['discount_base_price', 'stock_valued'])
        create_company()
        company = get_company()

        Uom = Model.get('product.uom')
        unit, = Uom.find([('name', '=', 'Unit')])
        Template = Model.get('product.template')
        template = Template(name='Product', type='goods', default_uom=unit)
        template.save()
        product, = template.products

        Location = Model.get('stock.location')
        supplier, = Location.find([('code', '=', 'SUP')])
        storage, = Location.find([('code', '=', 'STO')])
        Move = Model.get('stock.move')
        move = Move(product=product, quantity=2, from_location=supplier,
            to_location=storage, currency=company.currency)

        # With no discount, the unit price follows the base price.
        self.assertIsNone(move.discount_rate)
        move.base_price = Decimal('10')
        self.assertEqual(move.unit_price, Decimal('10'))
        move.base_price = Decimal('20')
        self.assertEqual(move.unit_price, Decimal('20'))
        self.assertEqual(move.discount_rate, Decimal('0'))

        # Editing the base price preserves the existing discount rate.
        move.discount_rate = Decimal('0.20')
        move.base_price = Decimal('15')
        self.assertEqual(move.unit_price, Decimal('12'))
        self.assertEqual(move.discount_rate, Decimal('0.20'))
        self.assertEqual(move.discount_amount, Decimal('3'))
        self.assertEqual(move.amount, Decimal('24'))
        move.save()
        move.reload()
        self.assertEqual(move.base_price, Decimal('15'))
        self.assertEqual(move.unit_price, Decimal('12'))
        self.assertEqual(move.discount_rate, Decimal('0.20'))

        # A zero base price is a valid price change.
        move.base_price = Decimal('0')
        self.assertEqual(move.unit_price, Decimal('0'))
        self.assertEqual(move.amount, Decimal('0'))
