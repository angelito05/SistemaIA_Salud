from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.alerta import AlertaCreate, AlertaRead

router = APIRouter(prefix="/alertas", tags=["Alertas"])


@router.get("/", response_model=List[AlertaRead])
def listar_alertas(
    paciente_id: int = None,
    activa: bool = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Retorna la lista de alertas médicas.
    Puede filtrarse por paciente o por estado (activa/resuelta).
    """
    # TODO: Implementar consulta a la base de datos
    return []


@router.get("/{alerta_id}", response_model=AlertaRead)
def obtener_alerta(alerta_id: int, db: Session = Depends(get_db)):
    """Retorna una alerta médica específica."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta no encontrada")


@router.post("/", response_model=AlertaRead, status_code=status.HTTP_201_CREATED)
def crear_alerta(alerta: AlertaCreate, db: Session = Depends(get_db)):
    """Crea una nueva alerta médica (generada por el agente de IA o manualmente)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="No implementado aún")


@router.patch("/{alerta_id}/resolver", response_model=AlertaRead)
def resolver_alerta(alerta_id: int, db: Session = Depends(get_db)):
    """Marca una alerta como resuelta."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="No implementado aún")
