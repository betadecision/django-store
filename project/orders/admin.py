from django.contrib import admin
from django.db.models import Count

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    can_delete = False
    extra = 0
    readonly_fields = ("product", "product_name", "unit_price", "quantity", "line_total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
        "status",
        "item_count",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "created_at")
    readonly_fields = ("total_amount", "created_at", "updated_at")
    search_fields = ("email", "full_name", "phone")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_item_count=Count("items"))

    @admin.display(description="Items", ordering="_item_count")
    def item_count(self, order):
        return order._item_count


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "quantity", "unit_price", "line_total")
    list_filter = ("order__status",)
    search_fields = ("order__email", "product_name")
    readonly_fields = ("order", "product", "product_name", "unit_price", "quantity", "line_total")
