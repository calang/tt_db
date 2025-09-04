#!/usr/bin/env python3
"""Load Prolog facts into SQLite database."""

import argparse
import os
import re
import sqlite3
import sys

#pylint: disable=too-many-locals
def extract_facts(prolog_file):
    """Extract Prolog facts from the specified Prolog file"""

    # Dictionary to store all extracted facts
    facts = {
        'constantes': [],
        'grupos': [],
        'materias': [],
        'profesores': [],
        'grupo_materias': [],
        'dias': [],
        'bloques': [],
        'lecciones': []
    }

    # Read the prolog file
    with open(prolog_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract constantes
    lecc_por_sem_match = re.search(r'lecc_por_sem\((\d+)\)', content)
    lecc_por_dia_match = re.search(r'lecc_por_dia\((\d+)\)', content)

    if lecc_por_sem_match:
        facts['constantes'].append(('lecc_por_sem', int(lecc_por_sem_match.group(1))))
    if lecc_por_dia_match:
        facts['constantes'].append(('lecc_por_dia', int(lecc_por_dia_match.group(1))))

    # Extract grupos
    grupo_pattern = r'grupo\((\d+),\s*(\w+)\)'
    grupos_matches = re.findall(grupo_pattern, content)
    facts['grupos'] = [(int(id), name) for id, name in grupos_matches]

    # Extract profesores
    prof_pattern = r'prof\((\d+),\s*(\w+)\)'
    prof_matches = re.findall(prof_pattern, content)
    facts['profesores'] = [(int(id), name) for id, name in prof_matches]

    # Extract materias (directly from materia/2 predicate)
    materia_pattern = r'materia\((\d+),\s*(\w+)\)'
    materia_matches = re.findall(materia_pattern, content)
    facts['materias'] = [(int(id), name) for id, name in materia_matches]

    # Extract dias
    dia_pattern = r'dia\(([a-z]\w*)\)'
    dia_matches = re.findall(dia_pattern, content)
    facts['dias'] = [(day,) for day in dia_matches]

    # Extract bloques
    bloque_pattern = r'bloque\((\d+)\)'
    bloque_matches = re.findall(bloque_pattern, content)
    facts['bloques'] = [(int(bloque),) for bloque in bloque_matches]

    # Extract lecciones
    leccion_pattern = r'leccion\(([a-z]\w*)\)'
    leccion_matches = re.findall(leccion_pattern, content)
    facts['lecciones'] = [(leccion,) for leccion in leccion_matches]

    # Extract grupo_materia_lecciones
    gml_pattern = r'grupo_materia_lecciones\((\d+),\s*(\w+|\d+),\s*(\w+),\s*(\d+)\)'
    gml_matches = re.findall(gml_pattern, content)

    # Convert grupo values if they are numeric strings
    grupo_materia_facts = []
    for gid, grupo, materia, lecciones in gml_matches:
        if grupo.isdigit():
            grupo = int(grupo)
        grupo_materia_facts.append((int(gid), grupo, materia, int(lecciones)))

    facts['grupo_materias'] = grupo_materia_facts

    return facts

#pylint: disable=too-many-statements,too-many-branches
def create_and_load_database(prolog_file, sql_file, db_file):
    """Create SQLite database and load data from Prolog facts"""

    # Create directory for the database if it doesn't exist
    db_dir = os.path.dirname(db_file)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Delete existing database if it exists
    if os.path.exists(db_file):
        os.remove(db_file)

    # Create connection to new database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    #pylint: disable=too-many-nested-blocks
    try:
        # Read the SQL schema from the specified SQL file and execute it
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_schema = f.read()

        cursor.executescript(sql_schema)

        # Extract facts from Prolog file
        facts = extract_facts(prolog_file)

        # Insert constantes
        try:
            cursor.executemany(
                "INSERT INTO constantes (name, value) VALUES (?, ?)",
                facts['constantes']
            )
        except sqlite3.Error as e:
            print(f"Error inserting constantes: {e}", file=sys.stderr)
            raise

        # Insert grupos
        try:
            cursor.executemany(
                "INSERT INTO grupos (id, nombre) VALUES (?, ?)",
                facts['grupos']
            )
        except sqlite3.Error as e:
            print(f"Error inserting grupos: {e}", file=sys.stderr)
            raise

        # Insert materias
        try:
            cursor.executemany(
                "INSERT INTO materias (id, nombre) VALUES (?, ?)",
                facts['materias']
            )
        except sqlite3.Error as e:
            print(f"Error inserting materias: {e}", file=sys.stderr)
            raise

        # Insert profesores
        try:
            cursor.executemany(
                "INSERT INTO profesores (id, nombre) VALUES (?, ?)",
                facts['profesores']
            )
        except sqlite3.Error as e:
            print(f"Error inserting profesores: {e}", file=sys.stderr)
            raise

        # Insert dias
        try:
            cursor.executemany(
                "INSERT INTO dias (nombre) VALUES (?)",
                facts['dias']
            )
        except sqlite3.Error as e:
            print(f"Error inserting dias: {e}", file=sys.stderr)
            raise

        # Insert bloques
        try:
            cursor.executemany(
                "INSERT INTO bloques (numero) VALUES (?)",
                facts['bloques']
            )
        except sqlite3.Error as e:
            print(f"Error inserting bloques: {e}", file=sys.stderr)
            raise

        # Insert lecciones
        try:
            cursor.executemany(
                "INSERT INTO lecciones (id) VALUES (?)",
                facts['lecciones']
            )
        except sqlite3.Error as e:
            print(f"Error inserting lecciones: {e}", file=sys.stderr)
            raise

        # Create mappings for foreign key references
        grupo_mapping = {}
        for gid, nombre in facts['grupos']:
            grupo_mapping[nombre] = gid

        materia_mapping = {nombre: id for id, nombre in facts['materias']}
        profesor_mapping = {nombre: id for id, nombre in facts['profesores']}

        # Insert grupo_materias with proper foreign keys
        for gid, grupo, materia, lecciones in facts['grupo_materias']:
            # Get grupo_id from mapping
            grupo_id = grupo_mapping.get(grupo)

            materia_id = materia_mapping.get(materia)

            if grupo_id is not None and materia_id is not None:
                try:
                    cursor.execute(
                        "INSERT INTO grupo_materias"
                        " (id, grupo_id, materia_id, lecciones) VALUES (?, ?, ?, ?)",
                        (gid, grupo_id, materia_id, lecciones)
                    )
                except sqlite3.Error as e:
                    print(f"Error inserting grupo_materias {gid}: {e}", file=sys.stderr)
                    raise

        # Extract prof_grupo_materia relations
        with open(prolog_file, 'r', encoding='utf-8') as f:
            content = f.read()

        pgm_pattern = r'prof_grupo_materia\((\w+),\s*(\w+|\d+),\s*(\w+)\)'
        pgm_matches = re.findall(pgm_pattern, content)

        # For each prof_grupo_materia relation
        for profesor, grupo, materia in pgm_matches:
            profesor_id = profesor_mapping.get(profesor)

            # Handle grupo which could be a string or a number
            if grupo.isdigit():
                grupo_id = grupo_mapping.get(int(grupo))
            else:
                grupo_id = grupo_mapping.get(grupo)

            materia_id = materia_mapping.get(materia)

            if profesor_id is not None and grupo_id is not None and materia_id is not None:
                # Find the grupo_materias entry ID
                try:
                    cursor.execute(
                        "SELECT id FROM grupo_materias WHERE grupo_id = ? AND materia_id = ?",
                        (grupo_id, materia_id)
                    )
                    result = cursor.fetchone()
                    if result:
                        grupo_materias_id = result[0]
                        # Insert into prof_grupo_materias
                        try:
                            cursor.execute(
                                "INSERT INTO prof_grupo_materias"
                                " (profesor_id, grupo_materias_id) VALUES (?, ?)",
                                (profesor_id, grupo_materias_id)
                            )
                        except sqlite3.IntegrityError:
                            pass  # Skip duplicate entries
                except sqlite3.Error as e:
                    print(
                        f"Error processing prof_grupo_materia for"
                        f" {profesor}, {grupo}, {materia}: {e}",
                        file=sys.stderr
                    )
                    raise

        # Create disponibilidad_profesores entries
        # Extract disp_prof_dia_bloque_leccion rules
        disp_patterns = [
            # Rule 1: angie on Wednesday for all blocks and lessons
            (profesor_mapping.get('angie'), 'mie', [1, 2, 3, 4], ['a', 'b']),
            # Rule 2: mpaula on Mon, Tue, Thu for all blocks and lessons
            (profesor_mapping.get('mpaula'), ['lun', 'mar', 'jue'], [1, 2, 3, 4], ['a', 'b']),
            # Rule 3: alonso on Wednesday for all blocks and lessons
            (profesor_mapping.get('alonso'), 'mie', [1, 2, 3, 4], ['a', 'b']),
            # Rule 4: All other professors for all days, blocks, and lessons
            ([profesor_mapping.get(p) for p in ['melissa', 'jonathan', 'gina', 'audry', 'daleana',
                                                'mayela', 'mjose', 'sol', 'alisson']],
             ['lun', 'mar', 'mie', 'jue', 'vie'], [1, 2, 3, 4], ['a', 'b'])
        ]

        # Process the patterns
        #pylint: disable=too-many-nested-blocks
        for rule in disp_patterns:
            prof_ids, dias, bloques, lecciones = rule

            # Convert to lists if not already
            if not isinstance(prof_ids, list):
                prof_ids = [prof_ids]
            if not isinstance(dias, list):
                dias = [dias]
            if not isinstance(bloques, list):
                bloques = [bloques]
            if not isinstance(lecciones, list):
                lecciones = [lecciones]

            # Generate all combinations
            for prof_id in prof_ids:
                for dia in dias:
                    for bloque in bloques:
                        for leccion in lecciones:
                            if prof_id is not None:
                                try:
                                    cursor.execute(
                                        "INSERT INTO disponibilidad_profesores"
                                        " (profesor_id, dia, bloque, leccion) VALUES (?, ?, ?, ?)",
                                        (prof_id, dia, bloque, leccion)
                                    )
                                except sqlite3.IntegrityError:
                                    print(
                                        f"IntegrityError inserting disponibilidad_profesores for"
                                        f" {prof_id}, {dia}, {bloque}, {leccion}: {e}",
                                        file=sys.stderr
                                    )
                                    raise
                                except sqlite3.Error as e:
                                    print(
                                        f"Error inserting disponibilidad_profesores for"
                                        f" {prof_id}, {dia}, {bloque}, {leccion}: {e}",
                                        file=sys.stderr
                                    )
                                    raise

        # Commit changes
        conn.commit()
        print(f"Database created and loaded successfully at {db_file}")

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Error creating database: {e}", file=sys.stderr)
        raise
    finally:
        # Close connection
        conn.close()


def main():
    """Main logic"""
    parser = argparse.ArgumentParser(description='Load Prolog facts into SQLite database.')
    parser.add_argument('prolog_file', help='Path to the Prolog facts file')
    parser.add_argument('sql_file', help='Path to the SQL schema file')
    parser.add_argument('db_file', help='Path for the output SQLite database file')

    args = parser.parse_args()

    # Validate input files exist
    if not os.path.isfile(args.prolog_file):
        print(f"Error: Prolog file '{args.prolog_file}' does not exist", file=sys.stderr)
        return 1

    if not os.path.isfile(args.sql_file):
        print(f"Error: SQL file '{args.sql_file}' does not exist", file=sys.stderr)
        return 1

    try:
        create_and_load_database(args.prolog_file, args.sql_file, args.db_file)
        return 0
    except Exception as e:  #pylint: disable=broad-exception-caught
        print(f"Error calling create_and_load_database: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
