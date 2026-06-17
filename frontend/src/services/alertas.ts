import api from "./api";

export interface Alerta {
  id: number;
  paciente_id: number;
  documento_id?: number;
  nivel: "Baja" | "Media" | "Alta" | "Crítica";
  titulo: string;
  descripcion: string;
  activa: boolean;
  resuelta_en?: string;
  creado_en: string;
}

export const alertasService = {
  /** Lista alertas, con filtros opcionales. */
  listar: async (pacienteId?: number, activa?: boolean, skip = 0, limit = 100): Promise<Alerta[]> => {
    const res = await api.get("/alertas", {
      params: { paciente_id: pacienteId, activa, skip, limit },
    });
    return res.data;
  },

  /** Obtiene una alerta por ID. */
  obtener: async (id: number): Promise<Alerta> => {
    const res = await api.get(`/alertas/${id}`);
    return res.data;
  },

  /** Marca una alerta como resuelta. */
  resolver: async (id: number): Promise<Alerta> => {
    const res = await api.patch(`/alertas/${id}/resolver`);
    return res.data;
  },
};
