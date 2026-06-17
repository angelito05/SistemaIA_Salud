from fastapi import APIRouter

from app.api.v1 import pacientes, documentos, alertas

# Router principal de la API v1
api_router = APIRouter(prefix="/api/v1")

# Incluir todos los sub-routers
api_router.include_router(pacientes.router)
api_router.include_router(documentos.router)
api_router.include_router(alertas.router)
