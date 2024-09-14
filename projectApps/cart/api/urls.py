from django.urls import path
from projectApps.cart.api.views import (
    OrderListCreateView,
    OrderDetailView,
    OrderItemListCreateView,
    OrderItemDetailView,
    OrderOptionListCreateView,
    OrderOptionDetailView,
)

app_name = "CartAPI"

urlpatterns = [
    # Order URLs
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    # OrderItem URLs
    path(
        "orders/<int:order_pk>/items/",
        OrderItemListCreateView.as_view(),
        name="orderitem-list-create",
    ),
    path(
        "orders/<int:order_pk>/items/<int:pk>/",
        OrderItemDetailView.as_view(),
        name="orderitem-detail",
    ),
    # OrderOption URLs
    path(
        "orders/<int:order_pk>/options/",
        OrderOptionListCreateView.as_view(),
        name="orderoption-list-create",
    ),
    path(
        "orders/<int:order_pk>/options/<int:pk>/",
        OrderOptionDetailView.as_view(),
        name="orderoption-detail",
    ),
]
