from decimal import Decimal

from django.test import TestCase

from catalog.models import Category, Product

from .models import Order, OrderItem


class OrderModelTests(TestCase):
    def setUp(self):
        quantity = 2


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
        self.order = Order.objects.create(
            email="zinaidamonster@gmail.com",
            full_name="vakulich Eugen",
            phone="380953336533",
            total_amount=Decimal(self.product.price * quantity),
        )

        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            unit_price=self.product.price,
            quantity=quantity,
            line_total=self.product.price * quantity
        )

    def test_order_str(self):
        self.assertEqual(
            str(self.order),
            f"Order #{self.order.pk} - zinaidamonster@gmail.com (new)",
        )
    
    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), "zenbook x 2")

    def test_snapshot(self):
        self.product.name = "vivobook"
        self.product.price = Decimal("300")
        self.product.slug = "asus-vivobook"
        self.product.save()
        
        order = OrderItem.objects.filter(product_name="vivobook")
        self.assertFalse(order.exists())

        product_item = Product.objects.get(name="vivobook")
        ordered_item = OrderItem.objects.get(product_name="zenbook")
        self.assertNotEqual(product_item.price, ordered_item.unit_price)
            
        
        




    



