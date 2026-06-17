"""
Servicio de OCR (Reconocimiento Óptico de Caracteres).

Estrategia de fallback:
    1. Intenta con Tesseract (local, gratuito).
    2. Si Tesseract falla o no está instalado, usa Azure Computer Vision (en la nube).

Dependencias:
    pip install pytesseract Pillow pdf2image azure-cognitiveservices-vision-computervision
"""

import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


async def procesar_documento_ocr(contenido_bytes: bytes, nombre_archivo: str) -> str:
    """
    Extrae el texto de un documento (imagen o PDF) usando OCR.

    Args:
        contenido_bytes: El contenido binario del archivo subido.
        nombre_archivo: Nombre del archivo (se usa para detectar el tipo).

    Returns:
        El texto extraído como cadena.
    """
    extension = Path(nombre_archivo).suffix.lower()

    if extension == ".pdf":
        return await _ocr_pdf(contenido_bytes)
    elif extension in {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"}:
        return await _ocr_imagen(contenido_bytes)
    else:
        raise ValueError(f"Tipo de archivo no soportado para OCR: {extension}")


async def _ocr_imagen(imagen_bytes: bytes) -> str:
    """Aplica OCR a una imagen usando Tesseract como motor principal."""
    try:
        import pytesseract
        from PIL import Image

        image = Image.open(io.BytesIO(imagen_bytes))
        # lang='spa' para español; ajusta según tus necesidades
        texto = pytesseract.image_to_string(image, lang="spa+eng")
        logger.info("OCR completado con Tesseract.")
        return texto.strip()

    except ImportError:
        logger.warning("Tesseract/Pillow no disponible. Usando Azure OCR como fallback.")
        return await _ocr_azure(imagen_bytes)
    except Exception as e:
        logger.error(f"Error en Tesseract: {e}. Usando Azure OCR como fallback.")
        return await _ocr_azure(imagen_bytes)


async def _ocr_pdf(pdf_bytes: bytes) -> str:
    """Convierte un PDF en imágenes y aplica OCR a cada página."""
    try:
        from pdf2image import convert_from_bytes

        paginas = convert_from_bytes(pdf_bytes, dpi=300)
        textos = []
        for i, pagina in enumerate(paginas):
            img_bytes = io.BytesIO()
            pagina.save(img_bytes, format="PNG")
            texto_pagina = await _ocr_imagen(img_bytes.getvalue())
            textos.append(f"--- Página {i + 1} ---\n{texto_pagina}")
            logger.info(f"OCR completado para página {i + 1}/{len(paginas)}.")

        return "\n\n".join(textos)

    except ImportError:
        logger.error("pdf2image no está instalado. Instala: pip install pdf2image")
        raise RuntimeError("No se puede procesar PDFs sin la librería pdf2image.")


async def _ocr_azure(imagen_bytes: bytes) -> str:
    """
    Fallback: Extrae texto con Azure Computer Vision Read API.
    Requiere: AZURE_COGNITIVE_ENDPOINT y AZURE_COGNITIVE_KEY en .env
    """
    from app.core.config import settings

    if not settings.AZURE_COGNITIVE_KEY or not settings.AZURE_COGNITIVE_ENDPOINT:
        raise RuntimeError(
            "No hay motor OCR disponible. "
            "Instala Tesseract o configura AZURE_COGNITIVE_KEY en .env"
        )

    try:
        import time
        from azure.cognitiveservices.vision.computervision import ComputerVisionClient
        from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
        from msrest.authentication import CognitiveServicesCredentials

        client = ComputerVisionClient(
            settings.AZURE_COGNITIVE_ENDPOINT,
            CognitiveServicesCredentials(settings.AZURE_COGNITIVE_KEY),
        )

        stream = io.BytesIO(imagen_bytes)
        respuesta = client.read_in_stream(stream, raw=True)
        operation_id = respuesta.headers["Operation-Location"].split("/")[-1]

        # Polling hasta que la operación termine
        while True:
            resultado = client.get_read_result(operation_id)
            if resultado.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                break
            time.sleep(1)

        texto_total = ""
        if resultado.status == OperationStatusCodes.succeeded:
            for page in resultado.analyze_result.read_results:
                for line in page.lines:
                    texto_total += line.text + "\n"

        logger.info("OCR completado con Azure Computer Vision.")
        return texto_total.strip()

    except Exception as e:
        logger.error(f"Error en Azure OCR: {e}")
        raise
