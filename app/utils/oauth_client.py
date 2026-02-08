"""OAuth configuration."""

from authlib.integrations.starlette_client import OAuth

from app.utils.settings import get_settings


oauth = OAuth()

oauth.register(
    name="google",
    client_id=get_settings().CLIENT_ID_GOOGLE,
    client_secret=get_settings().SECRET_GOOGLE,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)
