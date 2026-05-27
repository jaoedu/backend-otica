from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AddressViewSet, RegisterView, MeView, LoginView

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="addresses")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    # padrão do seu front:
    path("token/", LoginView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
] + router.urls
