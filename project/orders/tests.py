from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

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
            stock_quantity=10,
        )
        self.product_2 = Product.objects.create(
            name="TUF",
            price=Decimal("10.40"),
            slug="asus-tuf",
            category=self.notebook_category,
            stock_quantity=10,
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

    def test_create_order_requires_items(self):
        with self.assertRaises(ValueError):
            create_order(
                email="decisionbeta@gmail.com",
                full_name="eugen",
                phone="3603045345",
                items=[],
            )

    def test_create_order_rejects_quantity_above_stock(self):
        with self.assertRaises(ValueError):
            create_order(
                email="decisionbeta@gmail.com",
                full_name="eugen",
                phone="3603045345",
                items=[
                    {
                        "product": self.product,
                        "quantity": 11,
                    },
                ],
            )


class OrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="notebook", slug="notebook")
        self.product = Product.objects.create(
            name="zenbook",
            price=Decimal("10.30"),
            slug="asus-zenbook",
            category=self.category,
            stock_quantity=5,
        )

    def test_create_order_endpoint_creates_order(self):
        response = self.client.post(
            reverse("order-create"),
            {
                "email": "decisionbeta@gmail.com",
                "full_name": "eugen",
                "phone": "3603045345",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 2,
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get()
        self.assertEqual(order.total_amount, Decimal("20.60"))
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(response.data["id"], order.id)
        self.assertEqual(response.data["status"], Order.Status.NEW)
        self.assertEqual(response.data["total_amount"], "20.60")

    def test_create_order_endpoint_requires_items(self):
        response = self.client.post(
            reverse("order-create"),
            {
                "email": "decisionbeta@gmail.com",
                "full_name": "eugen",
                "phone": "3603045345",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertIn("items", response.data)

    def test_create_order_endpoint_rejects_out_of_stock_product(self):
        self.product.stock_quantity = 0
        self.product.save()

        response = self.client.post(
            reverse("order-create"),
            {
                "email": "decisionbeta@gmail.com",
                "full_name": "eugen",
                "phone": "3603045345",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 1,
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertIn("items", response.data)

    def test_create_order_endpoint_rejects_quantity_above_stock(self):
        response = self.client.post(
            reverse("order-create"),
            {
                "email": "decisionbeta@gmail.com",
                "full_name": "eugen",
                "phone": "3603045345",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 6,
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertIn("items", response.data)

    def test_create_order_endpoint_rejects_product_from_inactive_category(self):
        self.category.is_active = False
        self.category.save()

        response = self.client.post(
            reverse("order-create"),
            {
                "email": "decisionbeta@gmail.com",
                "full_name": "eugen",
                "phone": "3603045345",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 1,
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertIn("items", response.data)

    def test_create_order_endpoint_rejects_empty_items(self):
        response = self.client.post(
            reverse("order-create"),
            {
                "email": "decisionbeta@gmail.com",
                "full_name": "eugen",
                "phone": "3603045345",
                "items": [],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertIn("items", response.data)

    def test_create_order_endpoint_rejects_zero_quantity(self):
        response = self.client.post(
            reverse("order-create"),
            {
                "email": "decisionbeta@gmail.com",
                "full_name": "eugen",
                "phone": "3603045345",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 0,
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertIn("items", response.data)

    def test_create_order_endpoint_rejects_inactive_product(self):
        self.product.is_active = False
        self.product.save()

        response = self.client.post(
            reverse("order-create"),
            {
                "email": "decisionbeta@gmail.com",
                "full_name": "eugen",
                "phone": "3603045345",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 2,
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertIn("items", response.data)
