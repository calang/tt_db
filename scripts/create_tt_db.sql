-- Create tables for timetable database

-- run with
-- sqlite3 timetable.db < create_tt_db.sql


CREATE TABLE constantes (
    name TEXT PRIMARY KEY NOT NULL,
    value INTEGER NOT NULL
);

CREATE TABLE grupos (
    id INTEGER PRIMARY KEY NOT NULL,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE materias (
    id INTEGER PRIMARY KEY NOT NULL,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE profesores (
    id INTEGER PRIMARY KEY NOT NULL,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE grupo_materias (
    id INTEGER PRIMARY KEY NOT NULL,
    grupo_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    lecciones INTEGER NOT NULL,
    UNIQUE(grupo_id, materia_id),
    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);

CREATE TABLE prof_grupo_materias (
    profesor_id INTEGER NOT NULL,
    grupo_materias_id INTEGER NOT NULL,
    PRIMARY KEY (profesor_id, grupo_materias_id),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id),
    FOREIGN KEY (grupo_materias_id) REFERENCES grupo_materias(id)
);

CREATE TABLE dias (
    nombre TEXT PRIMARY KEY NOT NULL
);

CREATE TABLE bloques (
    numero INTEGER PRIMARY KEY NOT NULL
);

CREATE TABLE lecciones (
    id TEXT PRIMARY KEY NOT NULL
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