% module to handle rows in a SQLite database as Prolog facts


/*
Requirements: SWI-Prolog with prosqlite package installed.
to install the package:
?- pack_install(prosqlite).

to verify installation:
?- pack_list_installed.
*/

:- module(sqlite_facts, [
    open_db/1,
    close_db/0,
    constantes/2,
    grupos/2,
    materias/2,
    profesores/2,
    grupo_materias/4,
    prof_grupo_materias/3,
    dias/2,
    bloques/2,
    lecciones/2,
    disponibilidad_profesores/4,
    run/0
    ]).

:- table (
    constantes/2,
    grupos/2,
    materias/2,
    profesores/2,
    grupo_materias/4,
    prof_grupo_materias/3,
    dias/2,
    bloques/2,
    lecciones/2,
    disponibilidad_profesores/4
    ).

:- use_module([
    library(prosqlite)
    ]).

open_db(File) :-
    sqlite_connect(File, ttdb).

close_db :-
    sqlite_disconnect(ttdb).


constantes(Name, Value) :-
    sqlite_query('select * from constantes', Row),
    Row = row(Name, Value).

grupos(Id, Nombre) :-
    sqlite_query('select * from grupos', Row),
    Row = row(Id, Nombre).

materias(Id, Nombre) :-
    sqlite_query('select * from materias', Row),
    Row = row(Id, Nombre).

profesores(Id, Nombre) :-
    sqlite_query('select * from profesores', Row),
    Row = row(Id, Nombre).

grupo_materias(Id, GrupoId, MateriaId, Lecciones) :-
    sqlite_query('select * from grupo_materias', Row),
    Row = row(Id, GrupoId, MateriaId, Lecciones).

prof_grupo_materias(ProfesorId, GrupoId, MateriaId) :-
    sqlite_query('select * from prof_grupo_materias', Row),
    Row = row(ProfesorId, GrupoId, MateriaId).

dias(Id, Nombre) :-
    sqlite_query('select * from dias', Row),
    Row = row(Id, Nombre).

bloques(Id, Nombre) :-
    sqlite_query('select * from bloques', Row),
    Row = row(Id, Nombre).

lecciones(Id, Nombre) :-
    sqlite_query('select * from lecciones', Row),
    Row = row(Id, Nombre).

disponibilidad_profesores(ProfesorId, DiaId, BloqueId, LeccionId) :-
    sqlite_query('select * from disponibilidad_profesores', Row),
    Row = row(ProfesorId, DiaId, BloqueId, LeccionId).

run :-
    open_db('data/tt.db'),
    writeln('=== CONSTANTES ==='),
    (constantes(Name, Value),
     writeln(constantes(Name, Value)),
     fail ; true),
    writeln('=== GRUPOS ==='),
    (grupos(Id, Nombre),
     writeln(grupos(Id, Nombre)),
     fail ; true),
    writeln('=== MATERIAS ==='),
    (materias(Id, Nombre),
     writeln(materias(Id, Nombre)),
     fail ; true),
    writeln('=== PROFESORES ==='),
    (profesores(Id, Nombre),
     writeln(profesores(Id, Nombre)),
     fail ; true),
    writeln('=== GRUPO_MATERIAS ==='),
    (grupo_materias(Id, GrupoId, MateriaId, Lecciones),
     writeln(grupo_materias(Id, GrupoId, MateriaId, Lecciones)),
     fail ; true),
    writeln('=== PROF_GRUPO_MATERIAS ==='),
    (prof_grupo_materias(ProfesorId, GrupoId, MateriaId),
     writeln(prof_grupo_materias(ProfesorId, GrupoId, MateriaId)),
     fail ; true),
    writeln('=== DIAS ==='),
    (dias(Id, Nombre),
     writeln(dias(Id, Nombre)),
     fail ; true),
    writeln('=== BLOQUES ==='),
    (bloques(Id, Nombre),
     writeln(bloques(Id, Nombre)),
     fail ; true),
    writeln('=== LECCIONES ==='),
    (lecciones(Id, Nombre),
     writeln(lecciones(Id, Nombre)),
     fail ; true),
    writeln('=== DISPONIBILIDAD_PROFESORES ==='),
    (disponibilidad_profesores(ProfesorId, DiaId, BloqueId, LeccionId),
     writeln(disponibilidad_profesores(ProfesorId, DiaId, BloqueId, LeccionId)),
     fail ; true),
    close_db.

