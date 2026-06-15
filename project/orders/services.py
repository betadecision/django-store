from django.db import transaction

from .models import Order, OrderItem


@transaction.atomic
def create_order(*, email, full_name, phone, items):
    total_amount = 0
    order_items = []

    for item in items:
        product = item["product"]
        quantity = item["quantity"]
        line_total = product.price * quantity

        total_amount += line_total

        order_items.append(
            OrderItem(
                product=product,
                product_name=product.name,
                unit_price=product.price,
                quantity=quantity,
                line_total=line_total,
            )
        )

    order = Order.objects.create(
        email=email,
        full_name=full_name,
        phone=phone,
        total_amount=total_amount,
    )

    for order_item in order_items:
        order_item.order = order

    OrderItem.objects.bulk_create(order_items)

    return order


def cancel_order(order):
    order.status = Order.Status.CANCELLED
    order.save(update_fields=["status", "updated_at"])
    return order

