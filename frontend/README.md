# SistemaIA Salud — Frontend

Interfaz de usuario del Sistema de Inteligencia Artificial para Gestión de Salud, construida con **Next.js 15** y **React 19**.

## Estructura

```
src/
├── components/       # Componentes visuales reutilizables
│   ├── ui/           # Componentes base (botones, tarjetas, modales)
│   ├── pacientes/    # Componentes relacionados con pacientes
│   └── documentos/   # Componentes de carga y visualización de documentos
│
├── pages/            # Vistas / rutas de la aplicación
│   ├── index.tsx         → Dashboard principal
│   ├── expedientes/      → Gestión de expedientes médicos
│   └── carga-archivos/   → Carga y procesamiento de documentos
│
└── services/         # Conexión con la API del backend
    ├── api.ts            → Configuración base de Axios
    ├── pacientes.ts      → Servicios de pacientes
    ├── documentos.ts     → Servicios de documentos
    └── alertas.ts        → Servicios de alertas
```

## Desarrollo

```bash
npm install
npm run dev
```

Accede en: [http://localhost:3000](http://localhost:3000)

## Variables de entorno

Crea un archivo `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```
