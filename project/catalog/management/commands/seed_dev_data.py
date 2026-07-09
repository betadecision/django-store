from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Category
from catalog.models import Product


CATEGORIES = [
    {
        "name": "Laptops",
        "slug": "laptops",
        "description": "Portable computers for work, study, and everyday use.",
    },
    {
        "name": "Accessories",
        "slug": "accessories",
        "description": "Useful add-ons for a cleaner setup.",
    },
    {
        "name": "Services",
        "slug": "services",
        "description": "Setup and support services for digital products.",
    },
]

PRODUCTS = [
    {
        "category_slug": "laptops",
        "name": "ZenBook Air 14",
        "slug": "zenbook-air-14",
        "description": "Lightweight laptop with a bright display and all-day battery life.",
        "price": Decimal("39999.00"),
        "stock_quantity": 7,
    },
    {
        "category_slug": "laptops",
        "name": "TUF Gaming 15",
        "slug": "tuf-gaming-15",
        "description": "Performance laptop for gaming, design, and heavy multitasking.",
        "price": Decimal("52999.00"),
        "stock_quantity": 4,
    },
    {
        "category_slug": "accessories",
        "name": "USB-C Dock",
        "slug": "usb-c-dock",
        "description": "Compact dock with HDMI, USB, ethernet, and power delivery.",
        "price": Decimal("3499.00"),
        "stock_quantity": 15,
    },
    {
        "category_slug": "accessories",
        "name": "Wireless Mouse",
        "slug": "wireless-mouse",
        "description": "Quiet wireless mouse for office and travel setups.",
        "price": Decimal("899.00"),
        "stock_quantity": 24,
    },
    {
        "category_slug": "services",
        "name": "Laptop Setup Service",
        "slug": "laptop-setup-service",
        "description": "Initial OS setup, updates, account configuration, and basic app install.",
        "price": Decimal("1499.00"),
        "stock_quantity": 20,
    },
]


class Command(BaseCommand):
    help = "Create repeatable development catalog data."

    def handle(self, *args, **options):
        categories_by_slug = {}

        for category_data in CATEGORIES:
            category, _created = Category.objects.update_or_create(
                slug=category_data["slug"],
                defaults={
                    "name": category_data["name"],
                    "description": category_data["description"],
                    "is_active": True,
                },
            )
            categories_by_slug[category.slug] = category

        for product_data in PRODUCTS:
            category = categories_by_slug[product_data["category_slug"]]
            Product.objects.update_or_create(
                slug=product_data["slug"],
                defaults={
                    "category": category,
                    "name": product_data["name"],
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "stock_quantity": product_data["stock_quantity"],
                    "is_active": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(CATEGORIES)} categories and {len(PRODUCTS)} products."
            )
        )
