from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# ─── Motor de SQLAlchemy ────────────────────────────────────────────────────
engine = create_engine(
    settings.DATABASE_URL,
    # SQL Server recomienda pool_pre_ping para detectar conexiones muertas
    pool_pre_ping=True,
    # Tamaño del pool de conexiones
    pool_size=10,
    max_overflow=20,
    # Echo=True muestra el SQL generado en consola (útil para debug)
    echo=settings.DEBUG,
)

# ─── Sesión ─────────────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ─── Base para los modelos ORM ───────────────────────────────────────────────
Base = declarative_base()


# ─── Dependency de FastAPI ───────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """
    Dependency que provee una sesión de base de datos por request.
    Se cierra automáticamente al finalizar cada request (patrón yield).
    
    Uso en endpoints:
        def mi_endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Crea todas las tablas definidas en los modelos si no existen."""
    from app.models import sql_server  # noqa: F401 — importar para registrar los modelos
    Base.metadata.create_all(bind=engine)
