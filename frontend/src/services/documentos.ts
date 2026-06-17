import api from "./api";

export interface Documento {
  id: number;
  paciente_id: number;
  nombre_archivo: string;
  tipo_documento: "Laboratorio" | "Imagen" | "Receta" | "Historia Clínica" | "Otro";
  ruta_almacenamiento?: string;
  texto_extraido?: string;
  resumen_ia?: string;
  procesado: boolean;
  mime_type?: string;
  tamano_bytes?: number;
  creado_en: string;
}

export interface ResultadoUpload {
  mensaje: string;
  archivo: string;
  texto_ocr: string;
  analisis_ia: {
    tipo_documento: string;
    resumen: string;
    hallazgos_clave: string[];
    alertas: { nivel: string; titulo: string; descripcion: string }[];
    requiere_revision: boolean;
  };
}

export const documentosService = {
  /** Obtiene documentos, opcionalmente filtrados por paciente. */
  listar: async (pacienteId?: number, skip = 0, limit = 100): Promise<Documento[]> => {
    const res = await api.get("/documentos", {
      params: { paciente_id: pacienteId, skip, limit },
    });
    return res.data;
  },

  /** Obtiene un documento por ID. */
  obtener: async (id: number): Promise<Documento> => {
    const res = await api.get(`/documentos/${id}`);
    return res.data;
  },

  /**
   * Sube un archivo, aplica OCR y lo analiza con IA.
   * @param pacienteId - ID del paciente al que pertenece el documento
   * @param archivo - El archivo (File) seleccionado por el usuario
   * @param onProgress - Callback de progreso (0-100)
   */
  subir: async (
    pacienteId: number,
    archivo: File,
    onProgress?: (porcentaje: number) => void
  ): Promise<ResultadoUpload> => {
    const formData = new FormData();
    formData.append("file", archivo);

    const res = await api.post(`/documentos/upload?paciente_id=${pacienteId}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress: (evento) => {
        if (onProgress && evento.total) {
          onProgress(Math.round((evento.loaded * 100) / evento.total));
        }
      },
    });
    return res.data;
  },

  /** Elimina un documento por ID. */
  eliminar: async (id: number): Promise<void> => {
    await api.delete(`/documentos/${id}`);
  },
};
