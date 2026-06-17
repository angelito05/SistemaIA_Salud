"""
Modelos ORM de SQLAlchemy que mapean las tablas de SQL Server.

Tablas definidas:
    - Paciente        → dbo.Pacientes
    - Documento       → dbo.Documentos
    - Alerta          → dbo.Alertas
"""

import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    Enum as SAEnum,
    LargeBinary,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


# ─────────────────────────────────────────────────────────────────────────────
# Paciente
# ─────────────────────────────────────────────────────────────────────────────
class Paciente(Base):
    __tablename__ = "Pacientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    fecha_nacimiento = Column(DateTime, nullable=False)
    curp = Column(String(18), unique=True, index=True, nullable=True)
    sexo = Column(SAEnum("M", "F", "Otro", name="sexo_enum"), nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=True)
    direccion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relaciones
    documentos = relationship("Documento", back_populates="paciente", cascade="all, delete-orphan")
    alertas = relationship("Alerta", back_populates="paciente", cascade="all, delete-orphan")


# ─────────────────────────────────────────────────────────────────────────────
# Documento
# ─────────────────────────────────────────────────────────────────────────────
class Documento(Base):
    __tablename__ = "Documentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("Pacientes.id"), nullable=False, index=True)
    nombre_archivo = Column(String(255), nullable=False)
    tipo_documento = Column(
        SAEnum("Laboratorio", "Imagen", "Receta", "Historia Clínica", "Otro", name="tipo_doc_enum"),
        nullable=False,
        default="Otro",
    )
    ruta_almacenamiento = Column(String(500), nullable=True)   # Ruta en disco o URL en Azure Blob
    texto_extraido = Column(Text, nullable=True)               # Resultado del OCR
    resumen_ia = Column(Text, nullable=True)                   # Análisis del agente de IA
    mime_type = Column(String(100), nullable=True)
    tamano_bytes = Column(Integer, nullable=True)
    procesado = Column(Boolean, default=False, nullable=False)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relaciones
    paciente = relationship("Paciente", back_populates="documentos")
    alertas = relationship("Alerta", back_populates="documento")


# ─────────────────────────────────────────────────────────────────────────────
# Alerta
# ─────────────────────────────────────────────────────────────────────────────
class Alerta(Base):
    __tablename__ = "Alertas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("Pacientes.id"), nullable=False, index=True)
    documento_id = Column(Integer, ForeignKey("Documentos.id"), nullable=True)
    nivel = Column(
        SAEnum("Baja", "Media", "Alta", "Crítica", name="nivel_alerta_enum"),
        nullable=False,
        default="Baja",
    )
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    activa = Column(Boolean, default=True, nullable=False)
    resuelta_en = Column(DateTime, nullable=True)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relaciones
    paciente = relationship("Paciente", back_populates="alertas")
    documento = relationship("Documento", back_populates="alertas")
