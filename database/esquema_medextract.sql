-- ============================================================
-- ESQUEMA DE BASE DE DATOS: SistemaIA_Salud (SQL Server)
-- Descripción: Script de creación de tablas para el sistema
--              de gestión médica con IA.
-- ============================================================

USE master;
GO

-- Crear la base de datos si no existe
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'SistemaIA_Salud')
BEGIN
    CREATE DATABASE SistemaIA_Salud
    COLLATE Modern_Spanish_CI_AS;
END
GO

USE SistemaIA_Salud;
GO

-- ────────────────────────────────────────────────────────────
-- TABLA: Pacientes
-- ────────────────────────────────────────────────────────────
IF OBJECT_ID('dbo.Pacientes', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Pacientes (
        id                  INT IDENTITY(1,1)   PRIMARY KEY,
        nombre              NVARCHAR(100)       NOT NULL,
        apellido_paterno    NVARCHAR(100)       NOT NULL,
        apellido_materno    NVARCHAR(100)       NULL,
        fecha_nacimiento    DATE                NOT NULL,
        curp                CHAR(18)            NULL,
        sexo                CHAR(5)             NOT NULL
                                CHECK (sexo IN ('M', 'F', 'Otro')),
        telefono            NVARCHAR(20)        NULL,
        email               NVARCHAR(150)       NULL,
        direccion           NVARCHAR(MAX)       NULL,
        activo              BIT                 NOT NULL DEFAULT 1,
        creado_en           DATETIME2           NOT NULL DEFAULT SYSUTCDATETIME(),
        actualizado_en      DATETIME2           NULL,

        CONSTRAINT UQ_Pacientes_CURP  UNIQUE (curp),
        CONSTRAINT UQ_Pacientes_Email UNIQUE (email)
    );

    CREATE INDEX IX_Pacientes_Nombre ON dbo.Pacientes (apellido_paterno, nombre);
END
GO

-- ────────────────────────────────────────────────────────────
-- TABLA: Documentos
-- ────────────────────────────────────────────────────────────
IF OBJECT_ID('dbo.Documentos', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Documentos (
        id                      INT IDENTITY(1,1)   PRIMARY KEY,
        paciente_id             INT                 NOT NULL,
        nombre_archivo          NVARCHAR(255)       NOT NULL,
        tipo_documento          NVARCHAR(30)        NOT NULL DEFAULT 'Otro'
                                    CHECK (tipo_documento IN (
                                        'Laboratorio', 'Imagen', 'Receta',
                                        'Historia Clínica', 'Otro'
                                    )),
        ruta_almacenamiento     NVARCHAR(500)       NULL,
        texto_extraido          NVARCHAR(MAX)       NULL,      -- Resultado del OCR
        resumen_ia              NVARCHAR(MAX)       NULL,      -- Análisis del agente IA
        mime_type               NVARCHAR(100)       NULL,
        tamano_bytes            INT                 NULL,
        procesado               BIT                 NOT NULL DEFAULT 0,
        creado_en               DATETIME2           NOT NULL DEFAULT SYSUTCDATETIME(),

        CONSTRAINT FK_Documentos_Paciente
            FOREIGN KEY (paciente_id) REFERENCES dbo.Pacientes(id)
            ON DELETE CASCADE
    );

    CREATE INDEX IX_Documentos_Paciente ON dbo.Documentos (paciente_id);
    CREATE INDEX IX_Documentos_Tipo     ON dbo.Documentos (tipo_documento);
END
GO

-- ────────────────────────────────────────────────────────────
-- TABLA: Alertas
-- ────────────────────────────────────────────────────────────
IF OBJECT_ID('dbo.Alertas', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Alertas (
        id              INT IDENTITY(1,1)   PRIMARY KEY,
        paciente_id     INT                 NOT NULL,
        documento_id    INT                 NULL,
        nivel           NVARCHAR(10)        NOT NULL DEFAULT 'Baja'
                            CHECK (nivel IN ('Baja', 'Media', 'Alta', 'Crítica')),
        titulo          NVARCHAR(200)       NOT NULL,
        descripcion     NVARCHAR(MAX)       NOT NULL,
        activa          BIT                 NOT NULL DEFAULT 1,
        resuelta_en     DATETIME2           NULL,
        creado_en       DATETIME2           NOT NULL DEFAULT SYSUTCDATETIME(),

        CONSTRAINT FK_Alertas_Paciente
            FOREIGN KEY (paciente_id) REFERENCES dbo.Pacientes(id)
            ON DELETE CASCADE,

        CONSTRAINT FK_Alertas_Documento
            FOREIGN KEY (documento_id) REFERENCES dbo.Documentos(id)
            ON DELETE NO ACTION
    );

    CREATE INDEX IX_Alertas_Paciente ON dbo.Alertas (paciente_id);
    CREATE INDEX IX_Alertas_Activa   ON dbo.Alertas (activa, nivel);
END
GO

-- ────────────────────────────────────────────────────────────
-- DATOS DE PRUEBA (comentar en producción)
-- ────────────────────────────────────────────────────────────
INSERT INTO dbo.Pacientes (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, curp, sexo, telefono, email)
VALUES
    ('Juan', 'García', 'López',    '1985-06-15', 'GALJ850615HDFRCN04', 'M', '+52 55 1234 5678', 'juan.garcia@email.com'),
    ('María', 'Hernández', 'Ruiz', '1990-03-22', 'HERM900322MDFRZR01', 'F', '+52 55 8765 4321', 'maria.hernandez@email.com');
GO

PRINT '✅ Esquema de SistemaIA_Salud creado exitosamente.';
GO
