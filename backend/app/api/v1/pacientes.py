from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.paciente import PacienteCreate, PacienteRead, PacienteUpdate

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/", response_model=List[PacienteRead])
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retorna la lista de todos los pacientes registrados."""
    # TODO: Implementar consulta a la base de datos
    return []


@router.get("/{paciente_id}", response_model=PacienteRead)
def obtener_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Retorna los datos de un paciente específico por su ID."""
    # TODO: Implementar búsqueda por ID
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado")


@router.post("/", response_model=PacienteRead, status_code=status.HTTP_201_CREATED)
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    """Registra un nuevo paciente en el sistema."""
    # TODO: Implementar creación en base de datos
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="No implementado aún")


@router.put("/{paciente_id}", response_model=PacienteRead)
def actualizar_paciente(paciente_id: int, paciente: PacienteUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de un paciente existente."""
    # TODO: Implementar actualización en base de datos
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="No implementado aún")


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Elimina un paciente del sistema (soft-delete recomendado)."""
    # TODO: Implementar eliminación
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="No implementado aún")
