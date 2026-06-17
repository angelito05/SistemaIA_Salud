from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoDocumentoEnum(str, Enum):
    laboratorio = "Laboratorio"
    imagen = "Imagen"
    receta = "Receta"
    historia_clinica = "Historia Clínica"
    otro = "Otro"


# ─── Base ────────────────────────────────────────────────────────────────────
class DocumentoBase(BaseModel):
    paciente_id: int = Field(..., example=1)
    nombre_archivo: str = Field(..., max_length=255, example="resultado_laboratorio.pdf")
    tipo_documento: TipoDocumentoEnum = Field(TipoDocumentoEnum.otro, example="Laboratorio")
    mime_type: Optional[str] = Field(None, max_length=100, example="application/pdf")
    tamano_bytes: Optional[int] = Field(None, example=204800)


# ─── Crear ───────────────────────────────────────────────────────────────────
class DocumentoCreate(DocumentoBase):
    """Datos para registrar un documento (usualmente tras el upload y OCR)."""
    ruta_almacenamiento: Optional[str] = Field(None, example="/storage/documentos/1/resultado.pdf")
    texto_extraido: Optional[str] = None
    resumen_ia: Optional[str] = None


# ─── Leer ────────────────────────────────────────────────────────────────────
class DocumentoRead(DocumentoBase):
    id: int
    ruta_almacenamiento: Optional[str] = None
    texto_extraido: Optional[str] = None
    resumen_ia: Optional[str] = None
    procesado: bool
    creado_en: datetime

    class Config:
        from_attributes = True
