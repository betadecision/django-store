from decimal import Decimal

from django.test import TestCase

from catalog.models import Category, Product
from .models import Order, OrderItem
from .services import cancel_order, create_order


class OrderModelTests(TestCase):
    def setUp(self):
        self.quantity = 2

        self.notebook_category = Category.objects.create(
            name="notebook",
            slug="notebook",
        )
        self.product = Product.objects.create(
            name="zenbook",
            price=Decimal("10.30"),
            slug="asus-zenbook",
            category=self.notebook_category,
        )
        self.product_2 = Product.objects.create(
            name="TUF",
            price=Decimal("10.40"),
            slug="asus-tuf",
            category=self.notebook_category,
        )
        self.order = Order.objects.create(
            email="zinaidamonster@gmail.com",
            full_name="vakulich Eugen",
            phone="380953336533",
            total_amount=Decimal(self.product.price * self.quantity),
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            unit_price=self.product.price,
            quantity=self.quantity,
            line_total=self.product.price * self.quantity,
        )

    def test_order_str(self):
        self.assertEqual(
            str(self.order),
            f"Order #{self.order.pk} - zinaidamonster@gmail.com (new)",
        )

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), "zenbook x 2")

    def test_order_item_keeps_product_snapshot(self):
        self.product.name = "vivobook"
        self.product.price = Decimal("300.00")
        self.product.slug = "asus-vivobook"
        self.product.save()

        order_items = OrderItem.objects.filter(product_name="vivobook")
        self.assertFalse(order_items.exists())

        product_item = Product.objects.get(name="vivobook")
        ordered_item = OrderItem.objects.get(product_name="zenbook")
        self.assertNotEqual(product_item.price, ordered_item.unit_price)
        self.assertEqual(ordered_item.unit_price, Decimal("10.30"))

    def test_create_order_creates_order_with_items(self):
        create_order(
            email="decisionbeta@gmail.com",
            full_name="eugen",
            phone="3603045345",
            items=[
                {"product": self.product_2, "quantity": self.quantity},
                {"product": self.product, "quantity": self.quantity},
            ],
        )
        order = Order.objects.get(email="decisionbeta@gmail.com")

        self.assertEqual(order.total_amount, Decimal("41.40"))
        self.assertEqual(order.items.count(), 2)

        tuf_item = order.items.get(product_name="TUF")
        zenbook_item = order.items.get(product_name="zenbook")

        self.assertEqual(tuf_item.unit_price, Decimal("10.40"))
        self.assertEqual(tuf_item.quantity, 2)
        self.assertEqual(tuf_item.line_total, Decimal("20.80"))

        self.assertEqual(zenbook_item.unit_price, Decimal("10.30"))
        self.assertEqual(zenbook_item.quantity, 2)
        self.assertEqual(zenbook_item.line_total, Decimal("20.60"))

    def test_cancel_order_marks_order_as_cancelled(self):
        cancel_order(self.order)

        self.order.refresh_from_db()

        self.assertEqual(self.order.status, Order.Status.CANCELLED)
