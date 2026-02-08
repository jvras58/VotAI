"""Application startup and configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.authentication.router import router as auth_router
from app.api.user.router import router as user_router
from app.api.poll.router import router as poll_router
from app.utils.settings import get_settings

app = FastAPI(
    title="EleitorAI API",
    description="API para votação com autenticação OAuth",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url=get_settings().SWAGGER_DOCS_ROUTE,
    redoc_url=get_settings().SWAGGER_REDOCS_ROUTE,
)

# ----------------------------------
#  SESSION MIDDLEWARE (necessário para OAuth)
# ----------------------------------
app.add_middleware(SessionMiddleware, secret_key=get_settings().SESSION_SECRET_KEY)

# ----------------------------------
#  CORS MIDDLEWARE
# ----------------------------------
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------
#  ROUTERS
# ----------------------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(poll_router, prefix="/polls", tags=["Polls"])


@app.get("/")
def read_root():
    """Root endpoint to verify that the API is running."""
    return {"message": "Welcome to EleitorAI API!"}
