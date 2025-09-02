#!/usr/bin/env python3

"""Produce a SQLite DB creation script from a YAML spec which follows the db_spec_schema.yaml"""

from pathlib import Path
import sys
from typing import Any
import yaml

def type_to_sqlite(type_name: str) -> str:
    """Convert spec types to SQLite types."""
    type_map = {
        'string': 'TEXT',
        'number': 'REAL',
        'integer': 'INTEGER',
        'boolean': 'INTEGER'  # SQLite has no boolean, use INTEGER
    }
    return type_map.get(type_name, 'TEXT')

def generate_column_def(column: dict[str, Any]) -> str:
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

def generate_constraint(constraint: dict) -> str:
    """Generate SQLite constraint definition from spec."""
    constraint_type = constraint['type']

    if constraint_type in ('PRIMARY KEY', 'UNIQUE'):
        columns = ', '.join(constraint['columns'])
        return f"{constraint_type} ({columns})"

    if constraint_type == 'CHECK':
        return f"CHECK ({constraint['expression']})"

    if constraint_type == 'FOREIGN KEY':
        columns = ', '.join(constraint['columns'])
        ref_table = constraint['references']['table']
        ref_cols = ', '.join(constraint['references']['columns'])
        return f"FOREIGN KEY ({columns}) REFERENCES {ref_table}({ref_cols})"

    return ''

def generate_create_table(table: dict[str, Any]) -> str:
    """Generate CREATE TABLE statement from spec."""
    parts = [f"CREATE TABLE {table['name']} ("]

    # Add columns
    column_defs = [generate_column_def(col) for col in table['columns']]

    # Add table constraints
    if 'constraints' in table:
        for constraint in table['constraints']:
            constraint_def = generate_constraint(constraint)
            if constraint_def:
                column_defs.append(constraint_def)

    parts.append(',\n    '.join(column_defs))
    parts.append(');')

    return '\n    '.join(parts)

def generate_sqlite_ddl(spec_file: Path) -> str:
    """Generate complete SQLite DDL from spec file."""
    with open(spec_file, encoding='utf-8') as f:
        spec = yaml.safe_load(f)['DatabaseSpec']

    statements = [
        "-- Generated SQLite DDL",
        "PRAGMA encoding = 'UTF-8';",
        "PRAGMA foreign_keys = ON;",
        ""
    ]

    # Create tables
    for table in spec['tables']:
        statements.append(generate_create_table(table))
        statements.append("")

    return '\n'.join(statements)

def main() -> None:
    """Main logic"""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <spec_file.yaml>", file=sys.stderr)
        sys.exit(1)

    spec_file = Path(sys.argv[1])
    if not spec_file.exists():
        print(f"Error: File {spec_file} not found", file=sys.stderr)
        sys.exit(1)

    try:
        sql = generate_sqlite_ddl(spec_file)
        print(sql, flush=True)
    except (yaml.YAMLError, UnicodeError) as e:
        print(f"Error processing YAML file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
