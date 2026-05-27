import json

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from accounts.models import Address
from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderReadSerializer
from .serializers_checkout import CheckoutSerializer


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        data = request.data.copy()
        if isinstance(data.get("items"), str):
            try:
                data["items"] = json.loads(data["items"])
            except json.JSONDecodeError:
                raise ValidationError({"items": "Formato invalido."})

        s = CheckoutSerializer(data=data)
        s.is_valid(raise_exception=True)

        items = s.validated_data["items"]
        address = Address.objects.filter(
            id=s.validated_data["address_id"],
            user=request.user,
        ).first()
        if not address:
            raise ValidationError({"address_id": "Endereco nao encontrado."})

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                status="pending",
                address_label=address.label,
                address_zipcode=address.zipcode,
                address_street=address.street,
                address_number=address.number,
                address_complement=address.complement,
                address_neighborhood=address.neighborhood,
                address_city=address.city,
                address_state=address.state,
                prescription_image=request.FILES.get("prescription_image"),
                prescription_notes=s.validated_data.get("prescription_notes", ""),
            )

            for it in items:
                product = (
                    Product.objects.select_for_update()
                    .filter(id=it["product_id"], active=True)
                    .first()
                )
                if not product:
                    raise ValidationError(
                        {"product_id": "Produto não encontrado ou inativo."}
                    )

                if product.stock < it["quantity"]:
                    raise ValidationError(
                        {"stock": f"Estoque insuficiente para {product.name}."}
                    )

                # preço final congelado (promoção entra aqui)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=it["quantity"],
                    unit_price=product.final_price,
                )

                product.stock -= it["quantity"]
                product.save(update_fields=["stock"])

        return Response(
            OrderReadSerializer(order, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
