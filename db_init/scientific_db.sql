-- Script de Inicialización para la Base de Datos Científica (scientific_db.sql)

-- =========================================================================
-- 1. TAXONOMÍA
-- =========================================================================

-- Tabla de Rangos (Reino, Filo, Clase, etc.)
CREATE TABLE Rank (
    rank_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    hierarchy_level INTEGER UNIQUE NOT NULL, -- Para ordenar la jerarquía (e.g., 10=Reino, 70=Familia)
    extras JSONB
);

-- Tabla de Taxones (Entidad central)
CREATE TABLE Taxon (
    taxon_id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES Taxon(taxon_id), -- Jerarquía padre-hijo
    rank_id INTEGER NOT NULL REFERENCES Rank(rank_id),
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    extras JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Nombres (Válidos, Sinónimos, Comunes)
CREATE TABLE Taxon_Name (
    taxon_name_id SERIAL PRIMARY KEY,
    taxon_id INTEGER NOT NULL REFERENCES Taxon(taxon_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    name_type VARCHAR(50) NOT NULL, -- 'Válido', 'Sinónimo', 'Común'
    language VARCHAR(10) DEFAULT 'es',
    UNIQUE (taxon_id, name, name_type),
    is_active BOOLEAN DEFAULT TRUE,
    extras JSONB
);

-- Referencias externas (IDs en WoRMS, GBIF, etc.)
CREATE TABLE Taxon_External_Ref (
    external_ref_id SERIAL PRIMARY KEY,
    taxon_id INTEGER NOT NULL REFERENCES Taxon(taxon_id) ON DELETE CASCADE,
    database_name VARCHAR(100) NOT NULL, -- WoRMS, GBIF, FishBase
    external_id VARCHAR(255) NOT NULL,
    UNIQUE (database_name, external_id)
);


-- =========================================================================
-- 2. PERSONAS Y ORGANIZACIONES
-- =========================================================================

-- Tabla de Organizaciones (Publisher, Afiliación, Colaboración)
CREATE TABLE Organization (
    organization_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    address TEXT,
    extras JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Tipos de Documento (Paper, Informe, Libro, Dataset)
CREATE TABLE Document_Type (
    document_type_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de Usuarios (Persona - para autenticación y roles)
CREATE TABLE "User" (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    date_of_birth DATE,
    -- Rol de usuario: 'admin', 'moderator', 'normal'
    role VARCHAR(50) NOT NULL DEFAULT 'normal',
    -- Estudios académicos
    academic_studies TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    password_hash VARCHAR(255), -- Para la autenticación
    notes TEXT,
    extras JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Afiliación (N:M entre Persona y Organización)
CREATE TABLE Person_Affiliation (
    person_affiliation_id SERIAL PRIMARY KEY,
    person_id INTEGER NOT NULL REFERENCES "User"(user_id) ON DELETE CASCADE,
    organization_id INTEGER NOT NULL REFERENCES Organization(organization_id) ON DELETE CASCADE,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    UNIQUE (person_id, organization_id, is_current) -- Una persona, una afiliación actual por organización
);

-- =========================================================================
-- 3. DOCUMENTOS Y RELACIONES
-- =========================================================================

-- Tabla de Documentos (Ampliada para paper científico)
CREATE TABLE Document (
    document_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    doi VARCHAR(255) UNIQUE,
    url VARCHAR(255),
    abstract TEXT,
    publication_year INTEGER,
    volume VARCHAR(50),
    issue VARCHAR(50),
    pages VARCHAR(50),
    document_type_id INTEGER NOT NULL REFERENCES Document_Type(document_type_id),
    publisher_id INTEGER REFERENCES Organization(organization_id), -- Quién lo publica
    language VARCHAR(10) DEFAULT 'en',
    -- Campo para permisos de edición
    created_by_user_id INTEGER REFERENCES "User"(user_id), 
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    extras JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Autoría (N:M entre Documento y Persona/User)
CREATE TABLE Document_Authorship (
    document_id INTEGER NOT NULL REFERENCES Document(document_id) ON DELETE CASCADE,
    person_id INTEGER NOT NULL REFERENCES "User"(user_id) ON DELETE CASCADE,
    author_order INTEGER NOT NULL, -- Orden de los autores
    role VARCHAR(50), -- Autor, Editor, Contribuidor
    PRIMARY KEY (document_id, person_id)
);

-- Adjuntos de Documentos (PDFs, datasets, etc.)
CREATE TABLE Document_Attachment (
    attachment_id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES Document(document_id) ON DELETE CASCADE,
    file_path VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    description VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Palabras Clave
CREATE TABLE Keyword (
    keyword_id SERIAL PRIMARY KEY,
    word VARCHAR(100) UNIQUE NOT NULL
);

-- Relación N:M entre Documento y Palabra Clave
CREATE TABLE Document_Keyword (
    document_id INTEGER NOT NULL REFERENCES Document(document_id) ON DELETE CASCADE,
    keyword_id INTEGER NOT NULL REFERENCES Keyword(keyword_id) ON DELETE CASCADE,
    PRIMARY KEY (document_id, keyword_id)
);

-- Relación de Evidencia (N:M entre Taxón y Documento)
CREATE TABLE Taxon_Document (
    taxon_id INTEGER NOT NULL REFERENCES Taxon(taxon_id) ON DELETE CASCADE,
    document_id INTEGER NOT NULL REFERENCES Document(document_id) ON DELETE CASCADE,
    evidence_type VARCHAR(100), -- Taxonomía, Distribución, Mención simple
    PRIMARY KEY (taxon_id, document_id)
);

-- =========================================================================
-- 4. OCURRENCIAS (Opcional/Expandible con PostGIS)
-- =========================================================================

-- Registros geoespaciales
CREATE TABLE Occurrence (
    occurrence_id SERIAL PRIMARY KEY,
    taxon_id INTEGER NOT NULL REFERENCES Taxon(taxon_id) ON DELETE RESTRICT,
    latitude NUMERIC(10, 8) NOT NULL,
    longitude NUMERIC(11, 8) NOT NULL,
    event_date DATE,
    document_id INTEGER REFERENCES Document(document_id) ON DELETE SET NULL, -- Documento que reporta la ocurrencia
    notes TEXT,
    -- Si usas PostGIS, añade: geom GEOMETRY(Point, 4326)
    is_active BOOLEAN DEFAULT TRUE,
    extras JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);