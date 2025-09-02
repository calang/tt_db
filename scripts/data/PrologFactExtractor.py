import os
import re
import sqlite3

def extract_facts():
    """Extract Prolog facts from timetable_base.pl file"""
    
    # Dictionary to store all extracted facts
    facts = {
        'constantes': [],
        'grupos': [],
        'materias': set(),  # Using a set to avoid duplicates
        'profesores': [],
        'grupo_materias': [],
        'dias': [],
        'bloques': [],
        'lecciones': []
    }
    
    # Read the timetable_base.pl file
    with open('timetable_base.pl', 'r', encoding='utf-8') as f:
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
    
    # Extract dias
    dia_pattern = r'dia\((\w+)\)'
    dia_matches = re.findall(dia_pattern, content)
    facts['dias'] = [(day,) for day in dia_matches]
    
    # Extract bloques
    bloque_pattern = r'bloque\((\d+)\)'
    bloque_matches = re.findall(bloque_pattern, content)
    facts['bloques'] = [(int(bloque),) for bloque in bloque_matches]
    
    # Extract lecciones
    leccion_pattern = r'leccion\((\w+)\)'
    leccion_matches = re.findall(leccion_pattern, content)
    facts['lecciones'] = [(leccion,) for leccion in leccion_matches]
    
    # Extract grupo_materia_lecciones and collect materias
    gml_pattern = r'grupo_materia_lecciones\((\d+),\s*(\w+),\s*(\w+),\s*(\d+)\)'
    gml_matches = re.findall(gml_pattern, content)
    
    for id, grupo, materia, lecciones in gml_matches:
        facts['grupo_materias'].append((int(id), grupo, materia, int(lecciones)))
        facts['materias'].add(materia)
    
    # Extract materias from prof_grupo_materia
    pgm_pattern = r'prof_grupo_materia\((\w+),\s*(\w+|\d+),\s*(\w+)\)'
    pgm_matches = re.findall(pgm_pattern, content)
    
    for _, _, materia in pgm_matches:
        facts['materias'].add(materia)
    
    # Convert materias set to list with IDs
    facts['materias'] = [(i+1, materia) for i, materia in enumerate(sorted(facts['materias']))]
    
    return facts


def create_and_load_database():
    """Create SQLite database and load data from Prolog facts"""
    
    # Delete existing database if it exists
    if os.path.exists('timetable.db'):
        os.remove('timetable.db')
    
    # Create connection to new database
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    
    # Read the SQL schema from tt.sql and execute it
    with open('tt.sql', 'r') as f:
        sql_schema = f.read()
    
    cursor.executescript(sql_schema)
    
    # Extract facts from Prolog file
    facts = extract_facts()
    
    # Insert constantes
    cursor.executemany(
        "INSERT INTO constantes (name, value) VALUES (?, ?)",
        facts['constantes']
    )
    
    # Insert grupos
    cursor.executemany(
        "INSERT INTO grupos (id, nombre) VALUES (?, ?)",
        facts['grupos']
    )
    
    # Insert materias
    cursor.executemany(
        "INSERT INTO materias (id, nombre) VALUES (?, ?)",
        facts['materias']
    )
    
    # Insert profesores
    cursor.executemany(
        "INSERT INTO profesores (id, nombre) VALUES (?, ?)",
        facts['profesores']
    )
    
    # Insert dias
    cursor.executemany(
        "INSERT INTO dias (nombre) VALUES (?)",
        facts['dias']
    )
    
    # Insert bloques
    cursor.executemany(
        "INSERT INTO bloques (numero) VALUES (?)",
        facts['bloques']
    )
    
    # Insert lecciones
    cursor.executemany(
        "INSERT INTO lecciones (id) VALUES (?)",
        facts['lecciones']
    )
    
    # Create a mapping of materia names to IDs
    cursor.execute("SELECT id, nombre FROM materias")
    materia_mapping = {nombre: id for id, nombre in cursor.fetchall()}
    
    # Create a mapping of grupo names to IDs
    cursor.execute("SELECT id, nombre FROM grupos")
    grupo_mapping = {nombre: id for id, nombre in cursor.fetchall()}
    
    # Insert grupo_materias with proper foreign keys
    for id, grupo, materia, lecciones in facts['grupo_materias']:
        grupo_id = grupo_mapping.get(grupo) if isinstance(grupo, str) else grupo
        materia_id = materia_mapping.get(materia)
        
        if grupo_id is not None and materia_id is not None:
            cursor.execute(
                "INSERT INTO grupo_materias (id, grupo_id, materia_id, lecciones) VALUES (?, ?, ?, ?)",
                (id, grupo_id, materia_id, lecciones)
            )
    
    # Create prof_grupo_materias entries
    # Extract prof_grupo_materia relations
    with open('timetable_base.pl', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pgm_pattern = r'prof_grupo_materia\((\w+),\s*(\w+|\d+),\s*(\w+)\)'
    pgm_matches = re.findall(pgm_pattern, content)
    
    # Create a mapping of profesor names to IDs
    cursor.execute("SELECT id, nombre FROM profesores")
    profesor_mapping = {nombre: id for id, nombre in cursor.fetchall()}
    
    # For each prof_grupo_materia relation
    for profesor, grupo, materia in pgm_matches:
        profesor_id = profesor_mapping.get(profesor)
        grupo_id = grupo_mapping.get(grupo) if isinstance(grupo, str) else grupo
        materia_id = materia_mapping.get(materia)
        
        if profesor_id is not None and grupo_id is not None and materia_id is not None:
            # Find the grupo_materias entry ID
            cursor.execute(
                "SELECT id FROM grupo_materias WHERE grupo_id = ? AND materia_id = ?",
                (grupo_id, materia_id)
            )
            result = cursor.fetchone()
            if result:
                grupo_materias_id = result[0]
                # Insert into prof_grupo_materias
                cursor.execute(
                    "INSERT INTO prof_grupo_materias (profesor_id, grupo_materias_id) VALUES (?, ?)",
                    (profesor_id, grupo_materias_id)
                )
    
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
                            cursor.execute(
                                "INSERT INTO disponibilidad_profesores (profesor_id, dia, bloque, leccion) VALUES (?, ?, ?, ?)",
                                (prof_id, dia, bloque, leccion)
                            )
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("Database created and loaded successfully.")

if __name__ == "__main__":
    create_and_load_database()
