from rest_framework import serializers


class CheckoutItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CheckoutSerializer(serializers.Serializer):
    items = CheckoutItemSerializer(many=True)
    address_id = serializers.IntegerField()
    prescription_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=2000,
    )

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("items não pode ser vazio.")
        return items
