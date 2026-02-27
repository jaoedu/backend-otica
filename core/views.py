from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiExample


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Health"],
        summary="Health check da API",
        description=(
            "Endpoint de verificação rápida do serviço.\n\n"
            "- **Não exige autenticação**.\n"
            "- Usado por monitoramento, deploy e testes de conectividade."
        ),
        responses={
            200: OpenApiExample(
                "Resposta OK",
                value={"status": "ok", "service": "otica-api", "version": "v1"},
                response_only=True,
            )
        },
    )
    def get(self, request):
        return Response({"status": "ok", "service": "otica-api", "version": "v1"})
