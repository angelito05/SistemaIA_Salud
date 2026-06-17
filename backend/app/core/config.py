from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configuración central de la aplicación.
    Los valores se cargan automáticamente desde el archivo .env
    """

    # --- Aplicación ---
    APP_NAME: str = "SistemaIA Salud"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "cambia-esta-clave-en-produccion"

    # --- Base de Datos (SQL Server) ---
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"
    DB_HOST: str = "localhost"
    DB_PORT: int = 1433
    DB_NAME: str = "SistemaIA_Salud"
    DB_USER: str = "sa"
    DB_PASSWORD: str = ""

    # --- OpenAI / LLM ---
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MAX_TOKENS: int = 2048

    # --- Azure OCR (opcional) ---
    AZURE_COGNITIVE_ENDPOINT: str = ""
    AZURE_COGNITIVE_KEY: str = ""

    # --- CORS ---
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    @property
    def DATABASE_URL(self) -> str:
        """Genera la URL de conexión para SQLAlchemy con pyodbc."""
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?driver={self.DB_DRIVER.replace(' ', '+')}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Retorna una instancia cacheada de Settings para evitar múltiples lecturas del .env."""
    return Settings()


# Instancia global para importar directamente
settings = get_settings()
