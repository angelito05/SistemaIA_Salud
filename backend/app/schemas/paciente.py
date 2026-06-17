from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class SexoEnum(str, Enum):
    masculino = "M"
    femenino = "F"
    otro = "Otro"


# ─── Base ────────────────────────────────────────────────────────────────────
class PacienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, example="Juan")
    apellido_paterno: str = Field(..., min_length=1, max_length=100, example="García")
    apellido_materno: Optional[str] = Field(None, max_length=100, example="López")
    fecha_nacimiento: datetime = Field(..., example="1985-06-15T00:00:00")
    curp: Optional[str] = Field(None, min_length=18, max_length=18, example="GALJ850615HDFRCN04")
    sexo: SexoEnum = Field(..., example="M")
    telefono: Optional[str] = Field(None, max_length=20, example="+52 55 1234 5678")
    email: Optional[EmailStr] = Field(None, example="juan.garcia@email.com")
    direccion: Optional[str] = Field(None, example="Calle Reforma 123, CDMX")


# ─── Crear ───────────────────────────────────────────────────────────────────
class PacienteCreate(PacienteBase):
    """Datos requeridos para registrar un nuevo paciente."""
    pass


# ─── Actualizar (todos los campos opcionales) ─────────────────────────────────
class PacienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    apellido_paterno: Optional[str] = Field(None, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    fecha_nacimiento: Optional[datetime] = None
    curp: Optional[str] = Field(None, min_length=18, max_length=18)
    sexo: Optional[SexoEnum] = None
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    activo: Optional[bool] = None


# ─── Leer (respuesta de la API) ───────────────────────────────────────────────
class PacienteRead(PacienteBase):
    id: int
    activo: bool
    creado_en: datetime
    actualizado_en: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permite convertir modelos SQLAlchemy a Pydantic
