# 🕶 Backend Ótica API

API REST construída com **Django + DRF + PostgreSQL + Docker**, com autenticação JWT e documentação OpenAPI 3.

Projeto estruturado para:

- Desenvolvimento local com Docker
- Deploy futuro em VPS (DigitalOcean / AWS / Railway)
- Evolução para ambiente de produção com Gunicorn + Nginx
- Escalabilidade modular por domínio

---

# 🚀 Stack

- Python 3.12
- Django 6
- Django REST Framework
- PostgreSQL 16
- Docker & Docker Compose
- SimpleJWT (JWT Authentication)
- drf-spectacular (Swagger / OpenAPI 3)

---

# 📦 Ambiente Local (Desenvolvimento)

## 1️⃣ Clonar o projeto

```bash
git clone https://github.com/jaoedu/backend-otica.git
cd backend-otica
```

2️⃣ Subir containers
```bash
docker compose up -d --build
```
3️⃣ Rodar migrations

```bash
docker compose exec web python manage.py migrate
```
4️⃣ Criar superusuário
```bash

docker compose exec web python manage.py createsuperuser
```
🔎 Endpoints Principais
Método Rota Descrição
GET /api/v1/health/ Verifica status da API
POST /api/v1/auth/register/ Cria usuário
POST /api/v1/auth/login/ Gera access + refresh
POST /api/v1/auth/refresh/ Renova access
GET /api/v1/auth/me/ Dados do usuário autenticado
📘 Documentação

Swagger:

/api/schema/swagger/

Redoc:

/api/schema/redoc/
🏗 Arquitetura
config/ → Configurações globais
core/ → Rotas versionadas + health
users/ → Custom User
accounts/ → Autenticação JWT
products/ → Domínio de produtos (futuro)
orders/ → Domínio de pedidos (futuro)
🔐 Autenticação

Autenticação via JWT.

Header obrigatório para rotas protegidas:

Authorization: Bearer SEU_ACCESS_TOKEN
🐳 Docker

Desenvolvimento
```bash

docker compose up -d
Rebuild
docker compose up -d --build
Resetar banco (⚠ apaga dados)
docker compose down -v
docker compose up -d --build
```

🌍 Preparação para Produção

O projeto já está preparado para:

Separar .env

Trocar runserver por gunicorn

Usar Nginx como reverse proxy

Configurar HTTPS (Let's Encrypt)

🔹 Ajustes necessários antes do deploy real
1️⃣ Criar .env

Exemplo:

DEBUG=False
SECRET_KEY=sua_secret_key_segura
ALLOWED_HOSTS=seudominio.com
DB_NAME=otica
DB_USER=postgres
DB_PASSWORD=senha_segura
DB_HOST=db
DB_PORT=5432
2️⃣ Alterar settings.py

Usar os.environ

DEBUG=False

Configurar ALLOWED_HOSTS

🔹 Trocar runserver por Gunicorn

No Dockerfile (produção):

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
🔹 Estrutura futura ideal de produção
Internet
↓
Nginx
↓
Gunicorn (Django)
↓
PostgreSQL
🛠 Comandos Essenciais
Logs
docker compose logs -f web
Migrations
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
Testar API
curl http://localhost:8000/api/v1/health/
📌 Status do Projeto

✅ Docker configurado
✅ PostgreSQL persistente
✅ Custom User
✅ JWT
✅ Swagger
⬜ Products
⬜ Orders
⬜ Deploy produção

🧠 Roadmap

CRUD Products

CRUD Orders

Permissões por tipo de usuário

Paginação e filtros

Deploy VPS

CI/CD (GitHub Actions)

📄 Licença

Uso educacional e profissional.
