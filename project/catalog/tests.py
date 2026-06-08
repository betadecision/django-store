from rest_framework.test import APIClient
from rest_framework import status

from decimal import Decimal

from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404

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


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.notebook_category = Category.objects.create(name="notebook", slug="notebook")
        self.videocard_category = Category.objects.create(name="videocard", slug="videocard")
        self.mp3_player_category = Category.objects.create(name="mp3player", slug="mp3-player", is_active=False)
        Product.objects.create(name="zenbook", price=Decimal(10.3), slug="asus-zenbook", category=self.notebook_category)
        Product.objects.create(name="xduo", price=Decimal(14.5), slug="xduo", category=self.mp3_player_category)
        Product.objects.create(name="asus", price=Decimal(15.5), slug="asus", category=self.videocard_category)


        
        


    def test_product_list_returns_active_products(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("zenbook", [item["name"] for item in response.data])
        self.assertNotIn("TUF", [item["name"] for item in response.data])


    def test_product_list_returns_active_categories(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("videocard", [item["name"] for item in response.data])
        self.assertNotIn("mp3player", [item["name"] for item in response.data])

        
    def test_product_list_filtered_by_category(self):
        url = reverse("product-list")
        response = self.client.get(url, {"category":"notebook"})
        self.assertIn("zenbook", [item["name"] for item in response.data])
        self.assertNotIn("TUF", [item["name"] for item in response.data])

    
    def test_search_by_slug(self):
        url = reverse("product-detail", kwargs={"slug": "asus-zenbook"})
        response = self.client.get(url)
        self.assertEqual("asus-zenbook", response.data["slug"])






        
        
        