from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Address

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "label",
            "zipcode",
            "street",
            "number",
            "complement",
            "neighborhood",
            "city",
            "state",
            "is_default",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_state(self, value):
        value = value.strip().upper()
        if len(value) != 2:
            raise serializers.ValidationError("Use a sigla do estado com 2 letras.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if (
            request
            and request.method == "POST"
            and user
            and user.is_authenticated
            and not user.addresses.exists()
        ):
            attrs["is_default"] = True

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        return Address.objects.create(user=request.user, **validated_data)


class MeSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "phone", "addresses")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "phone")
        read_only_fields = ("id", "email")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "name", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            name=validated_data.get("name", ""),
            password=validated_data["password"],
        )
