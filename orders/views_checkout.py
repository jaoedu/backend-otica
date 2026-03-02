from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderReadSerializer
from .serializers_checkout import CheckoutSerializer


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        s = CheckoutSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        items = s.validated_data["items"]

        with transaction.atomic():
            order = Order.objects.create(user=request.user, status="pending")

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

        return Response(OrderReadSerializer(order).data, status=status.HTTP_201_CREATED)
