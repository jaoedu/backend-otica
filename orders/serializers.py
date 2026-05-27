from rest_framework import serializers
from .models import Order, OrderItem


class OrderProductReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = OrderProductReadSerializer(read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "unit_price", "line_total")

    def get_line_total(self, obj):
        return str(obj.total)


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    prescription_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "created_at",
            "items",
            "total",
            "address",
            "prescription_image_url",
            "prescription_notes",
        )

    def get_address(self, obj):
        return {
            "label": obj.address_label,
            "zipcode": obj.address_zipcode,
            "street": obj.address_street,
            "number": obj.address_number,
            "complement": obj.address_complement,
            "neighborhood": obj.address_neighborhood,
            "city": obj.address_city,
            "state": obj.address_state,
        }

    def get_total(self, obj):
        return str(obj.total)

    def get_prescription_image_url(self, obj):
        request = self.context.get("request")
        if obj.prescription_image and request:
            return request.build_absolute_uri(obj.prescription_image.url)
        return None
