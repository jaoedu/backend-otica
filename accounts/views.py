from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.utils import extend_schema, OpenApiExample

from .serializers import RegisterSerializer
from users.serializers import MeSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Cadastrar novo usuário",
        description=(
            "Cria um usuário no sistema.\n\n"
            "**Regras:**\n"
            "- `username` obrigatório\n"
            "- `password` mínimo 6 caracteres\n\n"
            "Depois do cadastro, use `/login/` para obter tokens JWT."
        ),
        request=RegisterSerializer,
        responses={
            201: MeSerializer,
            400: OpenApiExample(
                "Erro de validação",
                value={"password": ["Ensure this field has at least 6 characters."]},
                response_only=True,
            ),
        },
        examples=[
            OpenApiExample(
                "Exemplo de cadastro",
                value={
                    "username": "mota",
                    "email": "mota@email.com",
                    "password": "123456",
                },
                request_only=True,
            )
        ],
    )
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        return Response(MeSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    @extend_schema(
        tags=["Auth"],
        summary="Login (JWT)",
        description=(
            "Autentica o usuário e retorna:\n"
            "- `access`: token para acessar rotas protegidas\n"
            "- `refresh`: token para renovar o access"
        ),
        examples=[
            OpenApiExample(
                "Exemplo de login",
                value={"username": "mota", "password": "123456"},
                request_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    @extend_schema(
        tags=["Auth"],
        summary="Refresh token (JWT)",
        description="Recebe `refresh` e devolve um novo `access`.",
        examples=[
            OpenApiExample(
                "Exemplo refresh",
                value={"refresh": "SEU_REFRESH_TOKEN"},
                request_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Auth"],
        summary="Dados do usuário logado",
        description=(
            "Retorna os dados do usuário autenticado via JWT.\n\n"
            "Header obrigatório:\n"
            "`Authorization: Bearer <access_token>`"
        ),
        responses={200: MeSerializer},
    )
    def get(self, request):
        return Response(MeSerializer(request.user).data)
