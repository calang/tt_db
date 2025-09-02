#! /usr/bin/env python3

import pandas as pd

OUT_FILE = 'data/timetable.xlsx'

def create_timetable_excel():
    """
    Generates an Excel file with sheets corresponding to the timetable tables,
    populated with data from the prolog facts.
    """

    # Data from prolog facts
    constantes_facts = [
        ('lecc_por_sem', 40),
        ('lecc_por_dia', 8)
    ]

    grupos_facts = [
        (1, 'inter'), (2, 'trans'), (3, '1'), (4, '2'),
        (5, '3'), (6, '4'), (7, '5'), (8, '6')
    ]

    profesores_facts = [
        (1, 'alisson'), (2, 'alonso'), (3, 'angie'), (4, 'audry'),
        (5, 'daleana'), (6, 'gina'), (7, 'jonathan'), (8, 'mayela'),
        (9, 'melissa'), (10, 'mjose'), (11, 'mpaula'), (12, 'sol')
    ]

    materias_facts = [
        (1, 'edfís'), (2, 'infor'), (3, 'inglés'), (4, 'música'),
        (5, 'resto_sol'), (6, 'arte'), (7, 'ciencias'), (8, 'español'),
        (9, 'estsoc'), (10, 'ética'), (11, 'mate'), (12, 'francés'),
        (13, 'resto')
    ]

    grupo_materia_lecciones_facts = [
        (1, 'inter', 'edfís', 2), (2, 'inter', 'infor', 1), (3, 'inter', 'inglés', 11),
        (4, 'inter', 'música', 1), (5, 'trans', 'edfís', 2), (6, 'trans', 'infor', 1),
        (7, 'trans', 'inglés', 8), (8, 'trans', 'música', 1), (9, 'trans', 'resto_sol', 10),
        (11, '1', 'arte', 1), (12, '1', 'ciencias', 4), (13, '1', 'edfís', 2),
        (14, '1', 'español', 7), (15, '1', 'estsoc', 4), (16, '1', 'ética', 1),
        (17, '1', 'infor', 2), (18, '1', 'inglés', 8), (19, '1', 'mate', 8),
        (20, '1', 'música', 1), (21, '2', 'arte', 1), (22, '2', 'ciencias', 4),
        (23, '2', 'edfís', 2), (24, '2', 'español', 7), (25, '2', 'estsoc', 4),
        (26, '2', 'ética', 1), (27, '2', 'infor', 2), (28, '2', 'inglés', 10),
        (29, '2', 'mate', 8), (30, '2', 'música', 1), (31, '3', 'arte', 1),
        (32, '3', 'ciencias', 4), (33, '3', 'edfís', 2), (34, '3', 'español', 7),
        (35, '3', 'estsoc', 4), (36, '3', 'ética', 1), (37, '3', 'infor', 2),
        (38, '3', 'inglés', 10), (39, '3', 'mate', 8), (40, '3', 'música', 1),
        (41, '4', 'ciencias', 4), (42, '4', 'edfís', 2), (43, '4', 'español', 6),
        (44, '4', 'estsoc', 5), (45, '4', 'ética', 1), (46, '4', 'francés', 2),
        (47, '4', 'infor', 2), (48, '4', 'inglés', 9), (49, '4', 'mate', 8),
        (50, '4', 'música', 1), (51, '5', 'ciencias', 4), (52, '5', 'edfís', 2),
        (53, '5', 'español', 5), (54, '5', 'estsoc', 6), (55, '5', 'ética', 1),
        (56, '5', 'francés', 2), (57, '5', 'infor', 2), (58, '5', 'inglés', 9),
        (59, '5', 'mate', 8), (60, '5', 'música', 1), (61, '6', 'ciencias', 6),
        (62, '6', 'edfís', 2), (63, '6', 'español', 5), (64, '6', 'estsoc', 4),
        (65, '6', 'ética', 1), (66, '6', 'francés', 2), (67, '6', 'infor', 2),
        (68, '6', 'inglés', 9), (69, '6', 'mate', 8), (70, '6', 'música', 1)
    ]

    prof_grupo_materia_facts = [
        ('mpaula', 'inter', 'edfís'), ('jonathan', 'inter', 'infor'), ('mjose', 'inter', 'inglés'),
        ('alonso', 'inter', 'música'), ('alisson', 'inter', 'resto'), ('mpaula', 'trans', 'edfís'),
        ('jonathan', 'trans', 'infor'), ('audry', 'trans', 'inglés'), ('alonso', 'trans', 'música'),
        ('sol', 'trans', 'resto_sol'), ('alisson', 'trans', 'resto'), ('mjose', '1', 'arte'),
        ('sol', '1', 'ciencias'), ('mpaula', '1', 'edfís'), ('sol', '1', 'español'),
        ('sol', '1', 'estsoc'), ('mjose', '1', 'ética'), ('jonathan', '1', 'infor'),
        ('audry', '1', 'inglés'), ('sol', '1', 'mate'), ('alonso', '1', 'música'),
        ('sol', '1', 'resto'), ('alisson', '2', 'arte'), ('mjose', '2', 'ciencias'),
        ('mpaula', '2', 'edfís'), ('mjose', '2', 'español'), ('mjose', '2', 'estsoc'),
        ('alisson', '2', 'ética'), ('jonathan', '2', 'infor'), ('gina', '2', 'inglés'),
        ('mjose', '2', 'mate'), ('alonso', '2', 'música'), ('mjose', '2', 'resto'),
        ('mjose', '3', 'arte'), ('audry', '3', 'ciencias'), ('mpaula', '3', 'edfís'),
        ('audry', '3', 'español'), ('audry', '3', 'estsoc'), ('mjose', '3', 'ética'),
        ('jonathan', '3', 'infor'), ('gina', '3', 'inglés'), ('audry', '3', 'mate'),
        ('alonso', '3', 'música'), ('audry', '3', 'resto'), ('mayela', '4', 'ciencias'),
        ('mpaula', '4', 'edfís'), ('mayela', '4', 'español'), ('mayela', '4', 'estsoc'),
        ('alisson', '4', 'ética'), ('angie', '4', 'francés'), ('jonathan', '4', 'infor'),
        ('gina', '4', 'inglés'), ('mayela', '4', 'mate'), ('alonso', '4', 'música'),
        ('mayela', '4', 'resto'), ('mayela', '5', 'ciencias'), ('mpaula', '5', 'edfís'),
        ('daleana', '5', 'español'), ('daleana', '5', 'estsoc'), ('alisson', '5', 'ética'),
        ('angie', '5', 'francés'), ('jonathan', '5', 'infor'), ('gina', '5', 'inglés'),
        ('mayela', '5', 'mate'), ('alonso', '5', 'música'), ('mayela', '5', 'resto'),
        ('daleana', '6', 'ciencias'), ('mpaula', '6', 'edfís'), ('daleana', '6', 'español'),
        ('daleana', '6', 'estsoc'), ('alisson', '6', 'ética'), ('angie', '6', 'francés'),
        ('jonathan', '6', 'infor'), ('melissa', '6', 'inglés'), ('daleana', '6', 'mate'),
        ('alonso', '6', 'música'), ('daleana', '6', 'resto')
    ]

    dias_facts = [('lun',), ('mar',), ('mie',), ('jue',), ('vie',)]
    bloques_facts = [(1,), (2,), (3,), (4,)]
    lecciones_facts = [('a',), ('b',)]

    # Create dataframes
    df_constantes = pd.DataFrame(constantes_facts, columns=['name', 'value'])
    df_grupos = pd.DataFrame(grupos_facts, columns=['id', 'nombre'])
    df_profesores = pd.DataFrame(profesores_facts, columns=['id', 'nombre'])
    df_materias = pd.DataFrame(materias_facts, columns=['id', 'nombre'])
    df_dias = pd.DataFrame(dias_facts, columns=['nombre'])
    df_bloques = pd.DataFrame(bloques_facts, columns=['numero'])
    df_lecciones = pd.DataFrame(lecciones_facts, columns=['id'])

    # Helper maps for resolving IDs
    grupos_map = df_grupos.set_index('nombre')['id'].to_dict()
    materias_map = df_materias.set_index('nombre')['id'].to_dict()
    profesores_map = df_profesores.set_index('nombre')['id'].to_dict()

    # Process grupo_materias
    grupo_materias_data = [
        (id, grupos_map[grupo], materias_map[materia], lecciones)
        for id, grupo, materia, lecciones in grupo_materia_lecciones_facts
    ]
    df_grupo_materias = pd.DataFrame(
        grupo_materias_data,
        columns=['id', 'grupo_id', 'materia_id', 'lecciones']
    )

    # Process prof_grupo_materias
    gml_map = df_grupo_materias.set_index(['grupo_id', 'materia_id'])['id'].to_dict()
    
    # Add 'resto' to gml_map for groups
    for _, grupo_row in df_grupos.iterrows():
        lecc_por_sem = 40
        lecciones_sum = df_grupo_materias[df_grupo_materias['grupo_id'] == grupo_row['id']]['lecciones'].sum()
        resto_lecciones = lecc_por_sem - lecciones_sum
        if resto_lecciones > 0:
            resto_id = 100 + grupo_row['id']
            gml_map[(grupo_row['id'], materias_map['resto'])] = resto_id
            df_grupo_materias.loc[len(df_grupo_materias)] = [resto_id, grupo_row['id'], materias_map['resto'], resto_lecciones]


    prof_grupo_materias_data = []
    for prof, grupo, materia in prof_grupo_materia_facts:
        prof_id = profesores_map[prof]
        grupo_id = grupos_map[grupo]
        materia_id = materias_map[materia]
        g_m_id = gml_map.get((grupo_id, materia_id))
        if g_m_id:
            prof_grupo_materias_data.append((prof_id, g_m_id))

    df_prof_grupo_materias = pd.DataFrame(
        prof_grupo_materias_data,
        columns=['profesor_id', 'grupo_materias_id']
    )

    # Process disponibilidad_profesores
    disponibilidad = []
    # Rule 1
    for b in df_bloques['numero']:
        for l in df_lecciones['id']:
            disponibilidad.append((profesores_map['angie'], 'mie', b, l))
    # Rule 2
    for d in ['lun', 'mar', 'jue']:
        for b in df_bloques['numero']:
            for l in df_lecciones['id']:
                disponibilidad.append((profesores_map['mpaula'], d, b, l))
    # Rule 3
    for b in df_bloques['numero']:
        for l in df_lecciones['id']:
            disponibilidad.append((profesores_map['alonso'], 'mie', b, l))
    # Rule 4
    for p in ['melissa', 'jonathan', 'gina', 'audry', 'daleana', 'mayela', 'mjose', 'sol', 'alisson']:
        for d in df_dias['nombre']:
            for b in df_bloques['numero']:
                for l in df_lecciones['id']:
                    disponibilidad.append((profesores_map[p], d, b, l))

    df_disponibilidad_profesores = pd.DataFrame(
        disponibilidad,
        columns=['profesor_id', 'dia', 'bloque', 'leccion']
    )

    # Write to Excel
    with pd.ExcelWriter(OUT_FILE) as writer:
        df_constantes.to_excel(writer, sheet_name='constantes', index=False)
        df_grupos.to_excel(writer, sheet_name='grupos', index=False)
        df_materias.to_excel(writer, sheet_name='materias', index=False)
        df_profesores.to_excel(writer, sheet_name='profesores', index=False)
        df_grupo_materias.to_excel(writer, sheet_name='grupo_materias', index=False)
        df_prof_grupo_materias.to_excel(writer, sheet_name='prof_grupo_materias', index=False)
        df_dias.to_excel(writer, sheet_name='dias', index=False)
        df_bloques.to_excel(writer, sheet_name='bloques', index=False)
        df_lecciones.to_excel(writer, sheet_name='lecciones', index=False)
        df_disponibilidad_profesores.to_excel(writer, sheet_name='disponibilidad_profesores', index=False)

    print(f"Excel file '{OUT_FILE}' created successfully.")

if __name__ == '__main__':
    create_timetable_excel()
