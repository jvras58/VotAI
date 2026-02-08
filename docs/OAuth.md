[developers.google](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid)

## Passo 1: Crie/Selecione Projeto
1. Vá para [console.cloud.google.com](https://console.cloud.google.com).
2. Topo: Clique dropdown **"Select a project"** > **NEW PROJECT**.
3. Nome: "SaaS-Votacao" > **CREATE**. [support.google](https://support.google.com/cloud/answer/15549257?hl=en)

## Passo 2: Configure OAuth Consent Screen
1. Menu esquerdo: **APIs & Services** > **OAuth consent screen**.
2. User Type: **External** (para qualquer Google account) > **CREATE**.
3. **App info**:
   - App name: "Pesquisa Voto SaaS"
   - User support email: seuemail@gmail.com
   - App logo: opcional
   - App domain: seu-dominio.com (ou deixe em branco)
   - Authorized domains: adiciona `localhost` e `seuapp.onrender.com`
4. **Developer contact**: seuemail@gmail.com > **SAVE AND CONTINUE**.
5. Scopes: Adicione `.../auth/userinfo.email` e `.../auth/userinfo.profile` > **SAVE AND CONTINUE**.
6. Test users: Adicione seu email > **SAVE AND CONTINUE** > **BACK TO DASHBOARD**. [developers.google](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid)

## Passo 3: Crie OAuth Client ID
1. Ainda em **APIs & Services** > **Credentials** (🔑).
2. **+ CREATE CREDENTIALS** > **OAuth client ID**.
3. Application type: **Web application**.
4. Name: "FastAPI SaaS".
5. **Authorized redirect URIs** (crucial!):
   - Local: `http://localhost:8000/auth/google/callback`
   - Prod: `https://seuapp.onrender.com/auth/google/callback`
   - Adicione mais se precisar (ex: `http://127.0.0.1:8000/auth/google/callback`).
6. **CREATE** > Copie **Client ID** e **Client Secret**. [developers.google](https://developers.google.com/identity/protocols/oauth2/web-server)

## Passo 4: Ative APIs Necessárias
1. **APIs & Services** > **Library**.
2. Busque "Google People API" > **ENABLE** (para profile/email). [youtube](https://www.youtube.com/watch?v=Mi14foEa5PI)
3. Opcional: "Google+ API" se erro.

## Seu .env (FastAPI)
```
GOOGLE_CLIENT_ID=123456789-abcde.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456
```
No código:
```python
oauth.register(
    name='google',
    client_id=get_settings().CLIENT_ID_GOOGLE,
    client_secret=get_settings().SECRET_GOOGLE,
    ...
)
```

## Teste e Troubleshooting
- Rode local: Acesse `/auth/google/login` → deve redirecionar Google → callback.
- Erro "redirect_uri_mismatch": Verifique URIs exatos (sem / no final). [stackoverflow](https://stackoverflow.com/questions/75687525/google-oauth2-0-unintended-redirecting-to-http)
- "Unverified app": Normal em teste; users veem aviso.
- Prod: Use HTTPS (Render força); atualize URIs após deploy.