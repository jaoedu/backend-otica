from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from .views_checkout import CheckoutView

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
] + router.urls
