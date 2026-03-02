from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # mobile não deve ver inativo
        return (
            Product.objects.filter(active=True)
            .select_related("category")
            .prefetch_related("gallery", "attributes")
            .order_by("name")
        )

    def get_serializer_class(self):
        # lista leve na Home / detalhe completo na tela do produto
        if self.action == "list":
            return ProductListSerializer
        return ProductDetailSerializer
