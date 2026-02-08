EleitorAI - POC
================

Prova de conceito de uma API de votacao com login OAuth e controle de acesso via JWT.
O projeto esta organizado em app/ com separacao clara entre routers, controllers,
schemas e dependencias compartilhadas.

Funcionalidades
---------------
- Fluxo de login OAuth (Google) com callback que emite um JWT de acesso.
- Endpoint de voto protegido, validando JWT e bloqueando votos duplicados com Redis.
- Estrutura modular do FastAPI (routers/controllers/schemas).

Estrutura do Projeto
--------------------
app/
	startup.py
	api/
		dependencies.py
		authentication/
			controller.py
			router.py
			schemas.py
		poll/
			controller.py
			router.py
			schemas.py
		user/
			controller.py
			router.py
			schemas.py
	database/
		session.py
	utils/
		auth.py
		jwt.py
		oauth_client.py
		redis_client.py
		settings.py

Inicio Rapido
-------------
1) Instale as dependencias
	- Use seu gerenciador Python preferido. Exemplo:
	  uv sync

2) Crie um .env
	- Veja a secao de Variaveis de Ambiente abaixo.

3) Suba o Redis (necessario para evitar votos duplicados)
	- Exemplo:
	  docker compose up -d

4) Rode a API
	- Exemplo:
	  uv run uvicorn app.startup:app --reload

Variaveis de Ambiente
---------------------
Obrigatorias
- CLIENT_ID_GOOGLE
- SECRET_GOOGLE
- JWT_SECRET_KEY

Opcionais (valores padrao em settings.py)
- JWT_ALGORITHM (default: HS256)
- JWT_ACCESS_TOKEN_EXPIRE_SECONDS (default: 900)
- REDIS_HOST (default: localhost)
- REDIS_PORT (default: 6379)
- SWAGGER_DOCS_ROUTE (default: /docs)
- SWAGGER_REDOCS_ROUTE (default: /redoc)
- SESSION_SECRET_KEY (default: change-me-in-production)

Endpoints
---------
Auth
- GET /auth/{provider}/login
	Inicia o fluxo OAuth (ex.: /auth/google/login).

- GET /auth/{provider}/callback
	Trata o callback do OAuth e retorna dados do usuario e JWT:
	{
		"sub_hash": "...",
		"email": "...",
		"name": "...",
		"picture": "...",
		"access_token": "...",
		"token_type": "bearer"
	}

Poll
- POST /polls/{poll_id}/vote
	Endpoint protegido. Requer header:
	Authorization: Bearer <access_token>

	O voto e recusado se um duplicado for detectado via Redis.

Fluxo de Autenticacao (POC)
---------------------------
1) O cliente acessa /auth/google/login e completa o OAuth no provedor.
2) O provedor redireciona para /auth/google/callback.
3) O callback gera um JWT (sub_hash) e retorna para o cliente.
4) O cliente usa o JWT no header Authorization para votar.

Notas
-----
- Esta e uma POC. Segredos devem vir de variaveis de ambiente em producao.
- Persistencia de votos nao esta implementada; apenas a prevencao de duplicidade
	usando chaves no Redis.
```
