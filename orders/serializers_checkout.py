from rest_framework import serializers


class CheckoutItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CheckoutSerializer(serializers.Serializer):
    items = CheckoutItemSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("items não pode ser vazio.")
        return items
