from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductAttribute


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ("name", "value")


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("id", "alt_text", "image_url")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lista (vitrine): leve, rápida e perfeita pra Home do app.
    """

    image_url = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    is_on_sale = serializers.BooleanField(source="is_on_sale", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "brand",
            "price",
            "sale_price",
            "final_price",
            "is_on_sale",
            "stock",
            "image_url",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_final_price(self, obj):
        return str(obj.final_price)


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Detalhe (Amazon-like): galeria + atributos + descrição completa.
    """

    category = CategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    gallery = ProductImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    is_on_sale = serializers.BooleanField(source="is_on_sale", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "brand",
            "description",
            "price",
            "sale_price",
            "final_price",
            "is_on_sale",
            "stock",
            "active",
            "category",
            "image_url",
            "gallery",
            "attributes",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_final_price(self, obj):
        return str(obj.final_price)
