from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.documento import DocumentoCreate, DocumentoRead
from app.services.ocr_service import procesar_documento_ocr
from app.services.agent_service import analizar_documento_con_ia

router = APIRouter(prefix="/documentos", tags=["Documentos"])


@router.get("/", response_model=List[DocumentoRead])
def listar_documentos(paciente_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retorna los documentos médicos, opcionalmente filtrados por paciente."""
    # TODO: Implementar consulta a la base de datos
    return []


@router.get("/{documento_id}", response_model=DocumentoRead)
def obtener_documento(documento_id: int, db: Session = Depends(get_db)):
    """Retorna un documento médico específico."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def subir_documento(
    paciente_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Sube un documento médico (imagen o PDF), aplica OCR y lo analiza con IA.
    Soporta: PDF, PNG, JPG, TIFF.
    """
    contenido_bytes = await file.read()
    
    # Paso 1: Extraer texto con OCR
    texto_extraido = await procesar_documento_ocr(contenido_bytes, file.filename)
    
    # Paso 2: Analizar texto con el agente de IA
    resultado_ia = await analizar_documento_con_ia(texto_extraido, paciente_id)
    
    # TODO: Guardar el documento y resultado en la base de datos
    return {
        "mensaje": "Documento procesado exitosamente",
        "archivo": file.filename,
        "texto_ocr": texto_extraido[:500] + "...",  # Preview
        "analisis_ia": resultado_ia,
    }


@router.delete("/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_documento(documento_id: int, db: Session = Depends(get_db)):
    """Elimina un documento del sistema."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="No implementado aún")
