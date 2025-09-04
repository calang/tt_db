-- Generated SQLite DDL
PRAGMA encoding = 'UTF-8';
PRAGMA foreign_keys = ON;

CREATE TABLE constantes (
    name TEXT NOT NULL,
    value INTEGER NOT NULL,
    PRIMARY KEY (name)
    );

CREATE TABLE grupos (
    id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nombre)
    );

CREATE TABLE materias (
    id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nombre)
    );

CREATE TABLE profesores (
    id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nombre)
    );

CREATE TABLE grupo_materias (
    id INTEGER NOT NULL,
    grupo_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    lecciones INTEGER NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (grupo_id, materia_id),
    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
    );

CREATE TABLE prof_grupo_materias (
    profesor_id INTEGER NOT NULL,
    grupo_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    PRIMARY KEY (profesor_id, grupo_id, materia_id),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id),
    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
    );

CREATE TABLE dias (
    nombre TEXT NOT NULL,
    PRIMARY KEY (nombre)
    );

CREATE TABLE bloques (
    numero INTEGER NOT NULL,
    PRIMARY KEY (numero)
    );

CREATE TABLE lecciones (
    id TEXT NOT NULL,
    PRIMARY KEY (id)
    );

CREATE TABLE disponibilidad_profesores (
    profesor_id INTEGER NOT NULL,
    dia TEXT NOT NULL,
    bloque INTEGER NOT NULL,
    leccion TEXT NOT NULL,
    PRIMARY KEY (profesor_id, dia, bloque, leccion),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id),
    FOREIGN KEY (dia) REFERENCES dias(nombre),
    FOREIGN KEY (bloque) REFERENCES bloques(numero),
    FOREIGN KEY (leccion) REFERENCES lecciones(id)
    );

