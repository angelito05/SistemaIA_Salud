"""
Servicio del Agente de IA Médico.

Responsabilidades:
    - Analizar texto extraído por OCR usando un LLM (OpenAI GPT-4o).
    - Generar un resumen estructurado del documento médico.
    - Detectar anomalías y generar alertas cuando sea necesario.

Dependencias:
    pip install openai
"""

import json
import logging
from typing import Optional

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

# Cliente de OpenAI (inicializado de forma lazy)
_openai_client: Optional[AsyncOpenAI] = None


def _get_client() -> AsyncOpenAI:
    """Retorna el cliente de OpenAI, inicializándolo si es necesario."""
    global _openai_client
    if _openai_client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY no está configurada en el archivo .env")
        _openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _openai_client


# ─── Prompt del sistema ───────────────────────────────────────────────────────
SYSTEM_PROMPT = """
Eres MedExtract AI, un agente de inteligencia artificial especializado en análisis de documentos médicos.

Tu tarea es analizar el texto extraído de un documento médico y producir un JSON estructurado con:

1. **tipo_documento**: Tipo del documento ("Laboratorio", "Imagen", "Receta", "Historia Clínica", "Otro").
2. **resumen**: Resumen clínico conciso (máximo 150 palabras) en español.
3. **hallazgos_clave**: Lista de hallazgos importantes (valores fuera de rango, diagnósticos, medicamentos).
4. **alertas**: Lista de alertas detectadas. Cada alerta tiene:
   - nivel: "Baja" | "Media" | "Alta" | "Crítica"
   - titulo: Título corto de la alerta
   - descripcion: Explicación detallada
5. **requiere_revision**: true si el documento necesita revisión urgente por un médico, false si no.

Responde ÚNICAMENTE con el JSON válido, sin texto adicional.
"""


async def analizar_documento_con_ia(texto_ocr: str, paciente_id: int) -> dict:
    """
    Envía el texto extraído por OCR al LLM para análisis médico.

    Args:
        texto_ocr: Texto del documento extraído por OCR.
        paciente_id: ID del paciente (para contexto de logging).

    Returns:
        Diccionario con el análisis estructurado del documento.
    """
    if not texto_ocr or len(texto_ocr.strip()) < 20:
        logger.warning(f"Texto OCR muy corto para paciente {paciente_id}, saltando análisis IA.")
        return {
            "tipo_documento": "Otro",
            "resumen": "El documento no contiene suficiente texto para ser analizado.",
            "hallazgos_clave": [],
            "alertas": [],
            "requiere_revision": False,
        }

    client = _get_client()

    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=0.1,  # Baja temperatura para respuestas más deterministas
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Analiza el siguiente documento médico:\n\n{texto_ocr}",
                },
            ],
        )

        contenido = response.choices[0].message.content.strip()

        # Parsear el JSON de la respuesta
        resultado = json.loads(contenido)
        logger.info(
            f"Análisis IA completado para paciente {paciente_id}. "
            f"Alertas detectadas: {len(resultado.get('alertas', []))}"
        )
        return resultado

    except json.JSONDecodeError as e:
        logger.error(f"El LLM no retornó JSON válido: {e}")
        return {
            "tipo_documento": "Otro",
            "resumen": "Error al parsear la respuesta del agente de IA.",
            "hallazgos_clave": [],
            "alertas": [],
            "requiere_revision": True,
            "error": str(e),
        }
    except Exception as e:
        logger.error(f"Error al llamar a la API de OpenAI: {e}")
        raise


async def generar_resumen_expediente(historia_clinica: str) -> str:
    """
    Genera un resumen ejecutivo del expediente completo de un paciente.
    
    Args:
        historia_clinica: Texto consolidado con todos los documentos del paciente.
    
    Returns:
        Resumen narrativo del estado de salud del paciente.
    """
    client = _get_client()

    prompt = """
    Eres un médico internista experto. Con base en la historia clínica del paciente,
    genera un resumen ejecutivo de máximo 300 palabras que incluya:
    - Estado general de salud
    - Condiciones crónicas o diagnósticos relevantes
    - Medicamentos actuales
    - Recomendaciones de seguimiento
    
    Sé claro, conciso y profesional.
    """

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        max_tokens=600,
        temperature=0.2,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": historia_clinica},
        ],
    )

    return response.choices[0].message.content.strip()
