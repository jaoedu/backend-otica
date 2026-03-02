from django.urls import path, include
from .views import HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view()),
    path("auth/", include("accounts.urls")),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
]
