from decimal import Decimal
import unittest
from proteus import Model
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.modules.account.tests.tools import create_chart, get_accounts
from trytond.tests.tools import activate_modules
from trytond.tests.test_tryton import drop_db


class Test(unittest.TestCase):
    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):
        activate_modules([
            'discount_base_price', 'sale_price_list', 'sale_discount',
            ])

        create_company()
        company = get_company()

        create_chart(company)
        accounts = get_accounts(company)
        revenue = accounts['revenue']
        expense = accounts['expense']

        # Create parties
        Party = Model.get('party.party')
        party = Party(name="Party")
        party.save()

        # Create product
        ProductCategory = Model.get('product.category')
        account_category = ProductCategory(name="Account Category")
        account_category.accounting = True
        account_category.account_expense = expense
        account_category.account_revenue = revenue
        account_category.save()

        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])

        ProductTemplate = Model.get('product.template')
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'goods'
        template.account_category = account_category
        template.salable = True
        template.list_price = Decimal(10)
        template.save()
        product, = template.products

        # Create price list
        PriceList = Model.get('product.price_list')
        price_list = PriceList(name='Default', price='list_price')
        price_list_line = price_list.lines.new()
        price_list_line.quantity = 10
        price_list_line.formula = 'unit_price*0.90'
        price_list_line = price_list.lines.new()
        price_list_line.formula = 'unit_price'
        price_list.save()

        # Create a sale
        Sale = Model.get('sale.sale')
        sale = Sale()
        sale.party = party
        sale.invoice_method = 'order'

        line = sale.lines.new()
        line.product = product
        self.assertEqual(line.unit_price, Decimal('10.0000'))
        self.assertEqual(line.base_price, Decimal('10.0000'))
        line.quantity = 20
        self.assertEqual(line.unit_price, Decimal('10.0000'))
        self.assertEqual(line.base_price, Decimal('10.0000'))

        # Add price list, and check line prices from price list
        sale.price_list = price_list

        line = sale.lines.new()
        line.product = product
        self.assertEqual(line.unit_price, Decimal('10.0000'))
        self.assertEqual(line.base_price, Decimal('10.0000'))
        line.quantity = 20
        self.assertEqual(line.unit_price, Decimal('9.0000'))
        self.assertEqual(line.base_price, Decimal('9.0000'))

        # check on_change
        line.base_price = Decimal(8)
        self.assertEqual(line.unit_price, Decimal('8.0000'))
        line.unit_price = Decimal(4)
        self.assertEqual(line.base_price, Decimal('8.0000'))
        self.assertEqual(line.discount_rate, Decimal('0.5000'))
        self.assertEqual(line.discount, '50%')
