from django.contrib import admin

# Import the models that should be visible in the Django admin site.
from .models import Category
from .models import Product


# Register Category and connect it to the custom CategoryAdmin options below.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Columns shown on the category list page in admin.
    list_display = ("name", "slug", "is_active", "updated_at")
    # Sidebar filters for quickly narrowing the category list.
    list_filter = ("is_active",)
    # Fill slug from name automatically while editing in admin.
    prepopulated_fields = {"slug": ("name",)}
    # Fields used by the admin search box.
    search_fields = ("name", "slug")


# Register Product and connect it to the custom ProductAdmin options below.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns shown on the product list page in admin.
    list_display = (
        "name",
        "category",
        "price",
        "stock_quantity",
        "is_active",
        "updated_at",
    )
    # Sidebar filters for product availability and category.
    list_filter = ("is_active", "category")
    # Fetch category with each product in one query for the admin list page.
    list_select_related = ("category",)
    # Fill slug from name automatically while editing in admin.
    prepopulated_fields = {"slug": ("name",)}
    # Fields used by the admin search box.
    search_fields = ("name", "slug", "description")
