from django.urls import path

from . import views

urlpatterns = [
    path("orders/", views.CreateOrderView.as_view(), name="order-create"),
]