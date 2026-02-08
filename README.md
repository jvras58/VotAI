# EleitorAI - POC

**POC para pesquisas de intenção de voto com autenticação OAuth (Google), JWT, proteção anti-duplicidade via Redis e arquitetura modular FastAPI.**


## ✨ Destaques
- 🔐 **OAuth2 Google** com callback JWT automático
- 🛡️ **Anti-fraude**: 1 voto por conta Google + IP (Redis TTL 30 dias)
- 🏗️ **Modular**: Routers separados (auth, poll, user)
- 📊 **Pronto para DB**: Schemas Pydantic para votos/polls
- 🚀 **Deploy fácil**: Docker + Render/Vercel
- 📋 **Swagger**: `/docs` completo

## 📁 Estrutura
```
app/
├── startup.py              # App factory
├── api/
│   ├── dependencies.py     # get_oauth_user, get_remote_address
│   ├── authentication/     # OAuth controller/router/schemas
│   ├── poll/               # Voto controller/router/schemas
│   └── user/               # User controller/router/schemas
├── database/
│   └── session.py          # SQLAlchemy async (futuro)
├── utils/
│   ├── auth.py             # JWT utils
│   ├── oauth_client.py     # Authlib config
│   ├── redis_client.py     # Redis pool
│   └── settings.py         # Pydantic Settings
└── main.py                 # Entry point opcional
```

## 🚀 Início Rápido
### 1. Clone & Dependências
```bash
git clone <repo>
cd eleitorai
uv sync  # ou pip install -r requirements.txt
```

### 2. Redis (anti-duplicidade)
```bash
docker compose up -d redis
```

### 3. Config .env (Raiz)
```env
# Google OAuth (obrigatório - veja docs/setup)
CLIENT_ID_GOOGLE=123456789-abcde.apps.googleusercontent.com
SECRET_GOOGLE=GOCSPX-xyz123

# JWT (gere: openssl rand -hex 32)
JWT_SECRET_KEY=seu-super-secret-jwt-key-aqui

# Redis (default localhost:6379)
REDIS_HOST=localhost
REDIS_PORT=6379

# App (defaults ok)
JWT_ACCESS_TOKEN_EXPIRE_SECONDS=3600  # 1h
ORIGINS=http://localhost:3000,https://seuapp.onrender.com  # CORS
```
**Setup Google**: [Passo a passo completo](https://console.cloud.google.com/apis/credentials)

### 4. Rode API
```bash
uv run uvicorn app.startup:app --host 0.0.0.0 --port 8000 --reload
```
Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔌 Endpoints Principais

### Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/auth/google/login` | Inicia OAuth Google |
| `GET` | `/auth/google/callback` | **Retorna JWT**: `{"access_token": "...", "sub": "google-123", "email": "..."}` |

### Votação
| Método | Endpoint | Headers | Resposta |
|--------|----------|---------|----------|
| `POST` | `/polls/{poll_id}/vote` | `Authorization: Bearer {token}` | `{"sucesso": true}` ou `429 Duplicado` |

**Exemplo voto**:
```bash
curl -X POST "http://localhost:8000/polls/eleicao2026/vote" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 📋 Fluxo Completo
```
1. Frontend → /auth/google/login
2. Google Login → callback com user data
3. API → gera JWT com sub (ID único)
4. Frontend armazena JWT
5. Frontend → /polls/{id}/vote com Bearer JWT
6. API verifica Redis: hash(sub + poll_id + IP)
7. ✅ Voto salvo | ❌ 429 Duplicado
```

## 🛠️ Próximos Passos (Produção)
- [ ] PostgreSQL (alembic migrations)
- [ ] Frontend Next.js
- [ ] Docker: `docker compose up`
- [ ] Deploy Render: `render.yaml` pronto

## 🔒 Segurança & LGPD
- ✅ Apenas `hash(sub + IP)` no Redis (anonimizado)
- ✅ JWT expira 1h, refresh futuro
- ✅ CORS configurado
- ✅ Rate limiting incluso

## 📄 Licença
MIT - Use livremente!

**⭐ Star se ajudou!** _Feito com ❤️ para eleições BR 2026_