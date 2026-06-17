import api from "./api";

export interface Paciente {
  id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  fecha_nacimiento: string;
  curp?: string;
  sexo: "M" | "F" | "Otro";
  telefono?: string;
  email?: string;
  direccion?: string;
  activo: boolean;
  creado_en: string;
}

export interface PacienteCreate
  extends Omit<Paciente, "id" | "activo" | "creado_en"> {}

export const pacientesService = {
  /** Obtiene la lista de todos los pacientes. */
  listar: async (skip = 0, limit = 100): Promise<Paciente[]> => {
    const res = await api.get("/pacientes", { params: { skip, limit } });
    return res.data;
  },

  /** Obtiene un paciente por su ID. */
  obtener: async (id: number): Promise<Paciente> => {
    const res = await api.get(`/pacientes/${id}`);
    return res.data;
  },

  /** Crea un nuevo paciente. */
  crear: async (datos: PacienteCreate): Promise<Paciente> => {
    const res = await api.post("/pacientes", datos);
    return res.data;
  },

  /** Actualiza un paciente existente (parcialmente). */
  actualizar: async (id: number, datos: Partial<PacienteCreate>): Promise<Paciente> => {
    const res = await api.put(`/pacientes/${id}`, datos);
    return res.data;
  },

  /** Elimina un paciente por su ID. */
  eliminar: async (id: number): Promise<void> => {
    await api.delete(`/pacientes/${id}`);
  },
};
