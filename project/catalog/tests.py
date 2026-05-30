from decimal import Decimal

from django.db.models.deletion import ProtectedError
from django.test import TestCase

from .models import Category
from .models import Product


class CategoryModelTests(TestCase):
    def test_string_representation_returns_name(self):
        # Create a database row for the Category model.
        category = Category.objects.create(name="Books", slug="books")

        # __str__ controls how the object is shown in admin, shell, and logs.
        self.assertEqual(str(category), "Books")


class ProductModelTests(TestCase):
    def setUp(self):
        # setUp runs before each test method and prepares shared test data.
        self.category = Category.objects.create(name="Books", slug="books")

    def test_string_representation_returns_name(self):
        # Decimal is used for money values to avoid floating point rounding issues.
        product = Product.objects.create(
            category=self.category,
            name="Django Guide",
            slug="django-guide",
            price=Decimal("29.99"),
        )

        # Product.__str__ should return the product name.
        self.assertEqual(str(product), "Django Guide")

    def test_category_products_related_name_returns_products(self):
        # related_name="products" lets us access products from a category.
        product = Product.objects.create(
            category=self.category,
            name="Django Guide",
            slug="django-guide",
            price=Decimal("29.99"),
        )

        # This uses Category -> Product reverse relation: category.products.
        self.assertQuerySetEqual(self.category.products.all(), [product])

    def test_category_with_products_is_protected_from_delete(self):
        # Product.category uses on_delete=models.PROTECT.
        Product.objects.create(
            category=self.category,
            name="Django Guide",
            slug="django-guide",
            price=Decimal("29.99"),
        )

        # Deleting a category that still has products should raise ProtectedError.
        with self.assertRaises(ProtectedError):
            self.category.delete()
