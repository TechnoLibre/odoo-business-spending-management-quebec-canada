# -*- coding: utf-8 -*-

from odoo.tests import Form

from .test_sale_common import TestCommonSaleNoChart


class TestSaleOrder(TestCommonSaleNoChart):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrder, cls).setUpClass()
        super(TestSaleOrder, cls).setUpClassicProducts()
        cls.material_name = cls.env['sale.order'].with_context(tracking_disable=True).get_material_name()
        cls.work_load_name = cls.env['sale.order'].with_context(tracking_disable=True).get_work_load_name()

    def test_write_sale_order_line(self):
        """ Test sale order creation and write
            Expect section creation
        """
        expect_1_test = [
            (self.material_name, 'line_section'),
            (self.work_load_name, 'line_section'),
        ]

        expect_2_test = [
            (self.material_name, 'line_section'),
            (self.product_stock_order.display_name, False),
            (self.product_order.display_name, False),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
        ]

        form = Form(self.env['sale.order'].with_context(tracking_disable=True))
        form.partner_id = self.partner_customer_usd
        form.partner_invoice_id = self.partner_customer_usd
        form.partner_shipping_id = self.partner_customer_usd

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_1_test, result, 'Before writing')

        form = Form(so)

        # Insert line order
        with form.order_line.new() as line:
            line.product_id = self.service_deliver

        with form.order_line.new() as line:
            line.product_id = self.product_stock_order

        with form.order_line.new() as line:
            line.product_id = self.product_order

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_2_test, result, 'After writing')

    def test_write_update_product_to_service_sale_order_line(self):
        """ Test sale order creation and write with update product to service
            Expect section creation
        """
        expect_1_test = [
            (self.material_name, 'line_section'),
            (self.work_load_name, 'line_section'),
        ]

        expect_2_test = [
            (self.material_name, 'line_section'),
            (self.product_stock_order.display_name, False),
            (self.product_order.display_name, False),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
        ]

        expect_3_test = [
            (self.material_name, 'line_section'),
            (self.product_order.display_name, False),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
            (self.service_deliver.display_name, False),
        ]

        expect_4_test = [
            (self.material_name, 'line_section'),
            (self.product_order.display_name, False),
            (self.product_stock_order.display_name, False),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
        ]

        form = Form(self.env['sale.order'].with_context(tracking_disable=True))
        form.partner_id = self.partner_customer_usd
        form.partner_invoice_id = self.partner_customer_usd
        form.partner_shipping_id = self.partner_customer_usd

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_1_test, result, 'Before writing')

        form = Form(so)

        # Insert line order
        with form.order_line.new() as line:
            line.product_id = self.service_deliver

        with form.order_line.new() as line:
            line.product_id = self.product_stock_order

        with form.order_line.new() as line:
            line.product_id = self.product_order

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_2_test, result, 'After writing')

        form = Form(so)

        # Update line order
        with form.order_line.edit(1) as line:
            line.product_id = self.service_deliver

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_3_test, result, 'After edit product to service')

        form = Form(so)

        # Update line order
        with form.order_line.edit(3) as line:
            line.product_id = self.product_stock_order

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_4_test, result, 'After edit product to service')

    def test_write_update_product_to_service_with_note_sale_order_line(self):
        """ Test sale order creation and write with update product to service with note
            Expect section creation
        """
        section_1 = "section 1"
        note_1 = "note 1"
        note_2 = self.material_name
        note_3 = self.work_load_name
        expect_1_test = [
            (self.material_name, 'line_section'),
            (self.work_load_name, 'line_section'),
        ]

        expect_2_test = [
            (self.material_name, 'line_section'),
            (self.product_stock_order.display_name, False),
            (note_1, 'line_note'),
            (self.product_order.display_name, False),
            (note_2, 'line_note'),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
            (note_3, 'line_note'),
            (section_1, 'line_section'),
        ]

        expect_3_test = [
            (self.material_name, 'line_section'),
            (self.product_order.display_name, False),
            (note_2, 'line_note'),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
            (note_1, 'line_note'),
            (self.service_deliver.display_name, False),
            (note_3, 'line_note'),
            (section_1, 'line_section'),
        ]

        expect_4_test = [
            (self.material_name, 'line_section'),
            (self.product_order.display_name, False),
            (note_2, 'line_note'),
            (self.product_stock_order.display_name, False),
            (note_1, 'line_note'),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
            (note_3, 'line_note'),
            (section_1, 'line_section'),
        ]

        form = Form(self.env['sale.order'].with_context(tracking_disable=True))
        form.partner_id = self.partner_customer_usd
        form.partner_invoice_id = self.partner_customer_usd
        form.partner_shipping_id = self.partner_customer_usd

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_1_test, result, 'Before writing')

        form = Form(so)

        # Insert line order
        with form.order_line.new() as line:
            line.product_id = self.service_deliver

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_3

        with form.order_line.new() as line:
            line.display_type = "line_section"
            line.name = section_1

        with form.order_line.new() as line:
            line.product_id = self.product_stock_order

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_1

        with form.order_line.new() as line:
            line.product_id = self.product_order

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_2

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_2_test, result, 'After writing')

        form = Form(so)

        # Update line order
        with form.order_line.edit(1) as line:
            line.product_id = self.service_deliver

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_3_test, result, 'After edit product to service')

        form = Form(so)

        # Update line order
        with form.order_line.edit(4) as line:
            line.product_id = self.product_stock_order

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_4_test, result, 'After edit product to service')

    def test_write_update_product_to_service_sale_order_line(self):
        """ Test sale order creation and write with update product to service
            Expect section creation
        """
        expect_1_test = [
            (self.material_name, 'line_section'),
            (self.work_load_name, 'line_section'),
        ]

        expect_2_test = [
            (self.material_name, 'line_section'),
            (self.product_stock_order.display_name, False),
            (self.product_order.display_name, False),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
        ]

        expect_3_test = [
            (self.material_name, 'line_section'),
            (self.product_order.display_name, False),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
            (self.service_deliver.display_name, False),
        ]

        expect_4_test = [
            (self.material_name, 'line_section'),
            (self.product_order.display_name, False),
            (self.product_stock_order.display_name, False),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
        ]

        form = Form(self.env['sale.order'].with_context(tracking_disable=True))
        form.partner_id = self.partner_customer_usd
        form.partner_invoice_id = self.partner_customer_usd
        form.partner_shipping_id = self.partner_customer_usd

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_1_test, result, 'Before writing')

        form = Form(so)

        # Insert line order
        with form.order_line.new() as line:
            line.product_id = self.service_deliver

        with form.order_line.new() as line:
            line.product_id = self.product_stock_order

        with form.order_line.new() as line:
            line.product_id = self.product_order

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_2_test, result, 'After writing')

        form = Form(so)

        # Update line order
        with form.order_line.edit(1) as line:
            line.product_id = self.service_deliver

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_3_test, result, 'After edit product to service')

        form = Form(so)

        # Update line order
        with form.order_line.edit(3) as line:
            line.product_id = self.product_stock_order

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_4_test, result, 'After edit product to service')

    def test_write_with_new_product_sale_order_line(self):
        """ Test sale order creation and write with new product
            Expect section creation
        """
        section_1 = "section 1"
        note_1 = "note 1"
        note_2 = self.material_name
        note_3 = self.work_load_name

        expect_1_test = [
            (self.material_name, 'line_section'),
            (self.product_stock_order.display_name, False),
            (note_1, 'line_note'),
            (self.product_order.display_name, False),
            (note_2, 'line_note'),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
            (note_3, 'line_note'),
            (section_1, 'line_section'),
        ]

        expect_2_test = [
            (self.material_name, 'line_section'),
            (self.product_order.display_name, False),
            (self.product_stock_order.display_name, False),
            (note_1, 'line_note'),
            (self.product_order.display_name, False),
            (note_2, 'line_note'),
            (self.work_load_name, 'line_section'),
            (self.service_deliver.display_name, False),
            (note_3, 'line_note'),
            (self.service_deliver.display_name, False),
            (section_1, 'line_section'),
        ]

        form = Form(self.env['sale.order'].with_context(tracking_disable=True))
        form.partner_id = self.partner_customer_usd
        form.partner_invoice_id = self.partner_customer_usd
        form.partner_shipping_id = self.partner_customer_usd

        # Insert line order
        with form.order_line.new() as line:
            line.product_id = self.service_deliver

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_3

        with form.order_line.new() as line:
            line.display_type = "line_section"
            line.name = section_1

        with form.order_line.new() as line:
            line.product_id = self.product_stock_order

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_1

        with form.order_line.new() as line:
            line.product_id = self.product_order

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_2

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_1_test, result, 'Before writing')

        form = Form(so)

        # Remove all lines
        form.order_line.remove(8)
        form.order_line.remove(7)
        form.order_line.remove(6)
        form.order_line.remove(5)
        form.order_line.remove(4)
        form.order_line.remove(3)
        form.order_line.remove(2)
        form.order_line.remove(1)
        form.order_line.remove(0)

        # Add testing line
        with form.order_line.new() as line:
            line.product_id = self.product_order

        # Add all lines
        with form.order_line.new() as line:
            line.product_id = self.service_deliver

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_3

        with form.order_line.new() as line:
            line.display_type = "line_section"
            line.name = section_1

        with form.order_line.new() as line:
            line.product_id = self.product_stock_order

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_1

        with form.order_line.new() as line:
            line.product_id = self.product_order

        with form.order_line.new() as line:
            line.display_type = "line_note"
            line.name = note_2

        # Update line order
        with form.order_line.new() as line:
            line.product_id = self.service_deliver

        so = form.save()
        result = [(a.name, a.display_type) for a in so.order_line]
        self.assertEqual(expect_2_test, result, 'After writing')
