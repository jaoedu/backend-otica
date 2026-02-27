from django.urls import path, include
from .views import HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path("auth/", include("accounts.urls")),
]
