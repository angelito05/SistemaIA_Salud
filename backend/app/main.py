"""
Punto de entrada de la aplicación FastAPI - SistemaIA Salud.

Para ejecutar en desarrollo:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Documentación interactiva disponible en:
    http://localhost:8000/docs      (Swagger UI)
    http://localhost:8000/redoc     (ReDoc)
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_tables
from app.api.router import api_router

# ─── Logger ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ─── Lifespan (eventos de inicio/parada) ─────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ejecuta lógica de inicio y cierre de la aplicación."""
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}...")
    # Crear tablas en la base de datos si no existen
    create_tables()
    logger.info("✅ Conexión a base de datos establecida.")
    yield
    logger.info("🛑 Cerrando la aplicación...")


# ─── Instancia principal de FastAPI ──────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "API del Sistema de Inteligencia Artificial para Gestión de Salud. "
        "Procesa expedientes médicos con OCR y análisis por IA."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── Middleware CORS ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Registrar rutas de la API ────────────────────────────────────────────────
app.include_router(api_router)


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Sistema"])
async def health_check():
    """Endpoint de salud para verificar que el servidor está activo."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
    }
