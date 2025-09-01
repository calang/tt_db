% basic predicates for timetable

:- module(timetable_base, [
    lecc_por_sem/1,
    lecc_por_dia/1,
    grupo/2,
    aula/2,
    prof/2,
    grupo_materia_lecciones/4,
    prof_grupo_materia/3,
    disp_prof_dia_bloque_leccion/4,
    dia_bloque_leccion/3,
    dia/1,
    bloque/1,
    leccion/1
]).

% lecc_por_sem(?LS:int).
% LS es el total de lecciones por semana por grupo.
lecc_por_sem(40).

% lecc_por_dia(?LD:int).
% LD es total de lecciones por dia por grupo.
lecc_por_dia(8).

% grupo(?Id:int, ?Grupo:atomic).
grupo(1, inter).
grupo(2, trans).
grupo(3, 1).
grupo(4, 2).
grupo(5, 3).
grupo(6, 4).
grupo(7, 5).
grupo(8, 6).

% aula(?Id:int, ?Aula:atomic).
aula(1, inter).
aula(2, trans).
aula(3, 1).
aula(4, 2).
aula(5, 3).
aula(6, 4).
aula(7, 5).

% prof(?Id:int, ?Profesor:atom).
prof(1, alisson).
prof(2, alonso).
prof(3, angie).
prof(4, audry).
prof(5, daleana).
prof(6, gina).
prof(7, jonathan).
prof(8, mayela).
prof(9, melissa).
prof(10, mjose).
prof(11, mpaula).
prof(12, sol).

% grupo_materia_lecciones(+Id:int, +Grupo:atomic, ?Materia:atom, ?Cant_lecciones:int)
%
% El Grupo, de Materia requiere Cant_lecciones.

grupo_materia_lecciones(1, inter, edfís, 2).
grupo_materia_lecciones(2, inter, infor, 1).
grupo_materia_lecciones(3, inter, inglés, 11).
grupo_materia_lecciones(4, inter, música, 1).

grupo_materia_lecciones(5, trans, edfís, 2).
grupo_materia_lecciones(6, trans, infor, 1).
grupo_materia_lecciones(7, trans, inglés, 8).
grupo_materia_lecciones(8, trans, música, 1).
grupo_materia_lecciones(9, trans, resto_sol, 10).
% grupo_materia_lecciones(10, trans, resto_audry, 8).

grupo_materia_lecciones(11, 1, arte, 1).
grupo_materia_lecciones(12, 1, ciencias, 4).
grupo_materia_lecciones(13, 1, edfís, 2).
grupo_materia_lecciones(14, 1, español, 7).
grupo_materia_lecciones(15, 1, estsoc, 4).
grupo_materia_lecciones(16, 1, ética, 1).
grupo_materia_lecciones(17, 1, infor, 2).
grupo_materia_lecciones(18, 1, inglés, 8).
grupo_materia_lecciones(19, 1, mate, 8).
grupo_materia_lecciones(20, 1, música, 1).

grupo_materia_lecciones(21, 2, arte, 1).
grupo_materia_lecciones(22, 2, ciencias, 4).
grupo_materia_lecciones(23, 2, edfís, 2).
grupo_materia_lecciones(24, 2, español, 7).
grupo_materia_lecciones(25, 2, estsoc, 4).
grupo_materia_lecciones(26, 2, ética, 1).
grupo_materia_lecciones(27, 2, infor, 2).
grupo_materia_lecciones(28, 2, inglés, 10).
grupo_materia_lecciones(29, 2, mate, 8).
grupo_materia_lecciones(30, 2, música, 1).

grupo_materia_lecciones(31, 3, arte, 1).
grupo_materia_lecciones(32, 3, ciencias, 4).
grupo_materia_lecciones(33, 3, edfís, 2).
grupo_materia_lecciones(34, 3, español, 7).
grupo_materia_lecciones(35, 3, estsoc, 4).
grupo_materia_lecciones(36, 3, ética, 1).
grupo_materia_lecciones(37, 3, infor, 2).
grupo_materia_lecciones(38, 3, inglés, 10).
grupo_materia_lecciones(39, 3, mate, 8).
grupo_materia_lecciones(40, 3, música, 1).

grupo_materia_lecciones(41, 4, ciencias, 4).
grupo_materia_lecciones(42, 4, edfís, 2).
grupo_materia_lecciones(43, 4, español, 6).
grupo_materia_lecciones(44, 4, estsoc, 5).
grupo_materia_lecciones(45, 4, ética, 1).
grupo_materia_lecciones(46, 4, francés, 2).
grupo_materia_lecciones(47, 4, infor, 2).
grupo_materia_lecciones(48, 4, inglés, 9).
grupo_materia_lecciones(49, 4, mate, 8).
grupo_materia_lecciones(50, 4, música, 1).

grupo_materia_lecciones(51, 5, ciencias, 4).
grupo_materia_lecciones(52, 5, edfís, 2).
grupo_materia_lecciones(53, 5, español, 5).
grupo_materia_lecciones(54, 5, estsoc, 6).
grupo_materia_lecciones(55, 5, ética, 1).
grupo_materia_lecciones(56, 5, francés, 2).
grupo_materia_lecciones(57, 5, infor, 2).
grupo_materia_lecciones(58, 5, inglés, 9).
grupo_materia_lecciones(59, 5, mate, 8).
grupo_materia_lecciones(60, 5, música, 1).

grupo_materia_lecciones(61, 6, ciencias, 6).
grupo_materia_lecciones(62, 6, edfís, 2).
grupo_materia_lecciones(63, 6, español, 5).
grupo_materia_lecciones(64, 6, estsoc, 4).
grupo_materia_lecciones(65, 6, ética, 1).
grupo_materia_lecciones(66, 6, francés, 2).
grupo_materia_lecciones(67, 6, infor, 2).
grupo_materia_lecciones(68, 6, inglés, 9).
grupo_materia_lecciones(69, 6, mate, 8).
grupo_materia_lecciones(70, 6, música, 1).

% Update the dynamic clause for resto
grupo_materia_lecciones(Id, Grupo, resto, Resto) :-
    lecc_por_sem(Lecc_por_sem),
    grupo(IDG, Grupo),
    Id #= 100 + IDG *
    findall(
        Cantidad,
        (   dif(resto, Materia),
            grupo_materia_lecciones(_, Grupo, Materia, Cantidad)
        ),
        Lecciones
    ),
    sum_list(Lecciones, Suma_Cantidad),
    Resto #= Lecc_por_sem - Suma_Cantidad.


% prof_grupo_materia(?Profesor:atom, ?Grupo:atom, ?Materia:atom)
%
% Profesor es un profesor que está asignado a la materia Materia en el Grupo.
prof_grupo_materia(mpaula, inter, edfís).  % <-- ???
prof_grupo_materia(jonathan, inter, infor).
prof_grupo_materia(mjose, inter, inglés).
prof_grupo_materia(alonso, inter, música).
prof_grupo_materia(alisson, inter, resto).

prof_grupo_materia(mpaula, trans, edfís).
prof_grupo_materia(jonathan, trans, infor).
prof_grupo_materia(audry, trans, inglés).
prof_grupo_materia(alonso, trans, música).
prof_grupo_materia(sol, trans, resto_sol).
prof_grupo_materia(alisson, trans, resto).

prof_grupo_materia(mjose, 1, arte).
prof_grupo_materia(sol, 1, ciencias).
prof_grupo_materia(mpaula, 1, edfís).
prof_grupo_materia(sol, 1, español).
prof_grupo_materia(sol, 1, estsoc).
prof_grupo_materia(mjose, 1, ética).
prof_grupo_materia(jonathan, 1, infor).
prof_grupo_materia(audry, 1, inglés).
prof_grupo_materia(sol, 1, mate).
prof_grupo_materia(alonso, 1, música).
prof_grupo_materia(sol, 1, resto).

prof_grupo_materia(alisson, 2, arte).
prof_grupo_materia(mjose, 2, ciencias).
prof_grupo_materia(mpaula, 2, edfís).
prof_grupo_materia(mjose, 2, español).
prof_grupo_materia(mjose, 2, estsoc).
prof_grupo_materia(alisson, 2, ética).
prof_grupo_materia(jonathan, 2, infor).
prof_grupo_materia(gina, 2, inglés).
prof_grupo_materia(mjose, 2, mate).
prof_grupo_materia(alonso, 2, música).
prof_grupo_materia(mjose, 2, resto).

prof_grupo_materia(mjose, 3, arte).
prof_grupo_materia(audry, 3, ciencias).
prof_grupo_materia(mpaula, 3, edfís).
prof_grupo_materia(audry, 3, español).
prof_grupo_materia(audry, 3, estsoc).
prof_grupo_materia(mjose, 3, ética).
prof_grupo_materia(jonathan, 3, infor).
prof_grupo_materia(gina, 3, inglés).
prof_grupo_materia(audry, 3, mate).
prof_grupo_materia(alonso, 3, música).
prof_grupo_materia(audry, 3, resto).

prof_grupo_materia(mayela, 4, ciencias).
prof_grupo_materia(mpaula, 4, edfís).
prof_grupo_materia(mayela, 4, español).
prof_grupo_materia(mayela, 4, estsoc).
prof_grupo_materia(alisson, 4, ética).
prof_grupo_materia(angie, 4, francés).
prof_grupo_materia(jonathan, 4, infor).
prof_grupo_materia(gina, 4, inglés).
prof_grupo_materia(mayela, 4, mate).
prof_grupo_materia(alonso, 4, música).
prof_grupo_materia(mayela, 4, resto).

prof_grupo_materia(mayela, 5, ciencias).
prof_grupo_materia(mpaula, 5, edfís).
prof_grupo_materia(daleana, 5, español).
prof_grupo_materia(daleana, 5, estsoc).
prof_grupo_materia(alisson, 5, ética).
prof_grupo_materia(angie, 5, francés).
prof_grupo_materia(jonathan, 5, infor).
prof_grupo_materia(gina, 5, inglés).
prof_grupo_materia(mayela, 5, mate).
prof_grupo_materia(alonso, 5, música).
prof_grupo_materia(mayela, 5, resto).

prof_grupo_materia(daleana, 6, ciencias).
prof_grupo_materia(mpaula, 6, edfís).
prof_grupo_materia(daleana, 6, español).
prof_grupo_materia(daleana, 6, estsoc).
prof_grupo_materia(alisson, 6, ética).
prof_grupo_materia(angie, 6, francés).
prof_grupo_materia(jonathan, 6, infor).
prof_grupo_materia(melissa, 6, inglés).
prof_grupo_materia(daleana, 6, mate).
prof_grupo_materia(alonso, 6, música).
prof_grupo_materia(daleana, 6, resto).


% dia_bloque_leccion(?Dia:atom, ?Bloque:atom, ?Leccion:atom).
%
% Existe para un Dia un Bloque con una Leccion.

dia_bloque_leccion(Dia, Bloque, Leccion) :-
    dia(Dia),
    bloque(Bloque),
    leccion(Leccion).

dia(lun).
dia(mar).
dia(mie).
dia(jue).
dia(vie).

bloque(1).
bloque(2).
bloque(3).
bloque(4).

leccion(a).
leccion(b).


% disp_prof_dia_bloque_leccion(?Prof:atom, ?Dia:atom, ?Bloque:atom, ?Leccion:atom).
%
% Prof es un profesor, disponible el Dia, en Bloque y Leccion.
disp_prof_dia_bloque_leccion(angie, mie, B, L) :-
    member(B, [1,2,3,4]),
    member(L, [a,b]).
disp_prof_dia_bloque_leccion(mpaula, D, B, L) :-
    member(D, [lun,mar,jue]),
    bloque(B),
    leccion(L).
disp_prof_dia_bloque_leccion(alonso, mie, B, L) :-
    bloque(B),
    leccion(L).
disp_prof_dia_bloque_leccion(P, D, B, L) :-
    member(P, [melissa, jonathan, gina, audry, daleana, mayela, mjose, sol, alisson]),
    dia(D),
    bloque(B),
    leccion(L).
