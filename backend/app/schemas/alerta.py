from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class NivelAlertaEnum(str, Enum):
    baja = "Baja"
    media = "Media"
    alta = "Alta"
    critica = "Crítica"


# ─── Base ────────────────────────────────────────────────────────────────────
class AlertaBase(BaseModel):
    paciente_id: int = Field(..., example=1)
    documento_id: Optional[int] = Field(None, example=5)
    nivel: NivelAlertaEnum = Field(NivelAlertaEnum.baja, example="Alta")
    titulo: str = Field(..., max_length=200, example="Glucosa elevada")
    descripcion: str = Field(..., example="El resultado de laboratorio indica glucosa en 320 mg/dL, por encima del límite normal.")


# ─── Crear ───────────────────────────────────────────────────────────────────
class AlertaCreate(AlertaBase):
    """Datos para crear una nueva alerta médica."""
    pass


# ─── Leer ────────────────────────────────────────────────────────────────────
class AlertaRead(AlertaBase):
    id: int
    activa: bool
    resuelta_en: Optional[datetime] = None
    creado_en: datetime

    class Config:
        from_attributes = True
