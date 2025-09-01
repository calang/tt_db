#!/usr/bin/env python3

import sys
import yaml
from typing import Dict, List, Any
from pathlib import Path

def type_to_sqlite(type_name: str) -> str:
    """Convert spec types to SQLite types."""
    type_map = {
        'string': 'TEXT',
        'number': 'REAL',
        'integer': 'INTEGER',
        'boolean': 'INTEGER'  # SQLite has no boolean, use INTEGER
    }
    return type_map.get(type_name, 'TEXT')

def generate_column_def(column: Dict[str, Any]) -> str:
    """Generate SQLite column definition from spec."""
    parts = [
        column['name'],
        type_to_sqlite(column['type'])
    ]
    
    if column.get('not_null', False):
        parts.append('NOT NULL')
        
    if 'default' in column:
        default_val = column['default']
        if isinstance(default_val, str):
            default_val = f"'{default_val}'"
        elif isinstance(default_val, bool):
            default_val = '1' if default_val else '0'
        parts.append(f"DEFAULT {default_val}")
        
    return ' '.join(parts)

def generate_constraint(constraint: Dict[str, Any], table_name: str) -> str:
    """Generate SQLite constraint definition from spec."""
    constraint_type = constraint['type']
    
    if constraint_type in ('PRIMARY KEY', 'UNIQUE'):
        columns = ', '.join(constraint['columns'])
        return f"{constraint_type} ({columns})"
    
    elif constraint_type == 'CHECK':
        return f"CHECK ({constraint['expression']})"
        
    return ''

def generate_foreign_key(fk: Dict[str, Any]) -> str:
    """Generate SQLite foreign key definition from spec."""
    columns = ', '.join(fk['columns'])
    ref_table = fk['references']['table']
    ref_columns = ', '.join(fk['references']['columns'])
    
    return f"FOREIGN KEY ({columns}) REFERENCES {ref_table}({ref_columns})"

def generate_create_table(table: Dict[str, Any]) -> str:
    """Generate CREATE TABLE statement from spec."""
    parts = [f"CREATE TABLE {table['name']} ("]
    
    # Add columns
    column_defs = [generate_column_def(col) for col in table['columns']]
    
    # Add table constraints
    if 'constraints' in table:
        for constraint in table['constraints']:
            constraint_def = generate_constraint(constraint, table['name'])
            if constraint_def:
                column_defs.append(constraint_def)
    
    parts.append(',\n    '.join(column_defs))
    parts.append(');')
    
    return '\n    '.join(parts)

def generate_foreign_keys(spec: Dict[str, Any]) -> List[str]:
    """Generate ALTER TABLE statements for foreign keys."""
    if 'foreign_keys' not in spec:
        return []
        
    fk_statements = []
    for fk in spec['foreign_keys']:
        table_name = fk['table']
        fk_def = generate_foreign_key(fk)
        stmt = f"ALTER TABLE {table_name} ADD {fk_def};"
        fk_statements.append(stmt)
        
    return fk_statements

def generate_sqlite_ddl(spec_file: Path) -> str:
    """Generate complete SQLite DDL from spec file."""
    with open(spec_file) as f:
        spec = yaml.safe_load(f)['DatabaseSpec']
    
    statements = [
        "-- Generated SQLite DDL",
        "PRAGMA foreign_keys = ON;",
        ""
    ]
    
    # Create tables
    for table in spec['tables']:
        statements.append(generate_create_table(table))
        statements.append("")
    
    # Add foreign keys
    statements.extend(generate_foreign_keys(spec))
    
    return '\n'.join(statements)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <spec_file.yaml>")
        sys.exit(1)
        
    spec_file = Path(sys.argv[1])
    if not spec_file.exists():
        print(f"Error: File {spec_file} not found")
        sys.exit(1)
        
    sql = generate_sqlite_ddl(spec_file)
    print(sql)

if __name__ == '__main__':
    main()
