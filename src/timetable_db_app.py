#!/usr/bin/env python3

"""
CRUD application for the timetable database tables.
Includes tabs for all tables in the database with foreign key handling.
"""
#pylint: disable=too-many-locals,too-many-statements,too-many-branches
#pylint: disable=too-many-arguments,too-many-positional-arguments

# import os
import sqlite3
# import pprint as pp
# import sys

import dash
from dash import dcc, html, Input, Output, State, dash_table, ALL  #, callback
from dash.exceptions import PreventUpdate
import pandas as pd

from config.params import params

# --- Database setup ---
DB_FILE = params['DB_FILE']

def get_db_connection():
    """Establishes connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_table_schema(table_name):
    """Get the schema (column names and types) for a given table"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()
        return schema
    finally:
        conn.close()

def get_foreign_keys(table_name):
    """Get foreign key information for a given table"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()
        return foreign_keys
    finally:
        conn.close()

# def get_table_data(table_name):
#     """Get all data from a table"""
#     conn = get_db_connection()
#     try:
#         df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
#         return df.to_dict('records')
#     finally:
#         conn.close()

def get_table_data_with_fk_descriptions(table_name):
    """Get table data with foreign key descriptions joined in"""
    conn = get_db_connection()
    try:
        # Get foreign key information
        foreign_keys = get_foreign_keys(table_name)
        
        # Start with the base table
        query = f"SELECT {table_name}.*"
        from_clause = f"FROM {table_name}"
        
        # Add joins for each foreign key that references a table with 'name' or 'nombre'
        for fk in foreign_keys:
            ref_table = fk['table']
            ref_col = fk['to']
            fk_col = fk['from']
            
            # Check if the referenced table has a 'name' or 'nombre' column
            ref_schema = get_table_schema(ref_table)
            display_col = None
            
            for ref_column in ref_schema:
                if ref_column['name'].lower() in ['nombre', 'name']:
                    display_col = ref_column['name']
                    break
            
            if display_col:
                # Add the display column to the SELECT clause
                alias = f"{fk_col}_description"
                query += f", {ref_table}.{display_col} AS {alias}"
                # Add the LEFT JOIN
                from_clause += f" LEFT JOIN {ref_table} ON {table_name}.{fk_col} = {ref_table}.{ref_col}"
        
        full_query = f"{query} {from_clause}"
        df = pd.read_sql_query(full_query, conn)
        return df.to_dict('records')
    finally:
        conn.close()

def get_dropdown_options(table_name, id_col, display_col=None):
    """Get options for dropdowns from a table"""
    conn = get_db_connection()
    try:
        if display_col is None:
            display_col = id_col

        # Get data for the dropdown
        query = f"SELECT {id_col}, {display_col} FROM {table_name}"
        df = pd.read_sql_query(query, conn)

        # Format options for dropdown
        # Note: use row.iloc[index] instead of row[col_name]
        # because when display_col == id_col row[col_name]
        # returns a two-column Series instead of a single row value
        options = [
            {'label': str(row.iloc[1]),
             'value': row.iloc[0]
             }
            for _, row in df.iterrows()
        ]
        return options
    finally:
        conn.close()

# --- Dash App ---
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Define the tables in the database
tables = [
    'constantes', 'grupos', 'materias', 'profesores', 'grupo_materias',
    'prof_grupo_materias', 'dias', 'bloques', 'lecciones', 'disponibilidad_profesores'
]

# Create tabs for each table
tabs = dcc.Tabs(
    id='tabs',
    value=tables[0],
    children=[dcc.Tab(label=table.replace('_', ' ').title(), value=table) for table in tables]
)

# --- App Layout ---
app.layout = html.Div([
    html.H1('Timetable Database Management'),

    tabs,

    html.Div(id='tab-content'),
])

# --- Dynamic Tab Content ---
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    """Renders the content for each tab based on the selected table"""

    # Get schema information for the table
    schema = get_table_schema(tab)
    foreign_keys = get_foreign_keys(tab)

    # Create column configurations for the data table
    columns = []
    for column in schema:
        col_name = column['name']
        columns.append({'name': col_name.replace('_', ' ').title(), 'id': col_name})
        
        # Check if this column is a foreign key and add description column right after it
        for fk in foreign_keys:
            if fk['from'] == col_name:
                ref_table = fk['table']
                
                # Check if the referenced table has a 'name' or 'nombre' column
                ref_schema = get_table_schema(ref_table)
                display_col = None
                
                for ref_column in ref_schema:
                    if ref_column['name'].lower() in ['nombre', 'name']:
                        display_col = ref_column['name']
                        break
                
                if display_col:
                    # Add a column for the foreign key description right after the FK column
                    desc_col_id = f"{col_name}_description"
                    desc_col_name = f"{col_name.replace('_', ' ').title()} {display_col.title()}"
                    columns.append({'name': desc_col_name, 'id': desc_col_id})
                break

    # Create mapping for column types to input types
    col_type_to_input_type = {
        'integer': 'number',
        'number': 'number',
        'text': 'text',
        'string': 'text'
    }

    # Create input fields for each column
    input_fields = []
    for column in schema:
        col_name = column['name']
        col_type = column['type'].lower()

        # Check if this column is a foreign key
        is_foreign_key = False
        fk_info = None
        for fk in foreign_keys:
            if fk['from'] == col_name:
                is_foreign_key = True
                fk_info = fk
                break

        if is_foreign_key:
            # For foreign keys, create a dropdown with options from the referenced table
            ref_table = fk_info['table']
            ref_col = fk_info['to']

            # Get the primary key and name column for the referenced table
            ref_schema = get_table_schema(ref_table)
            display_col = None

            # Try to find a 'name' or 'nombre' column for display
            for ref_column in ref_schema:
                if ref_column['name'].lower() in ['nombre', 'name']:
                    display_col = ref_column['name']
                    break

            dropdown_options = get_dropdown_options(ref_table, ref_col, display_col)

            input_field = html.Div([
                html.Label(f"{col_name.replace('_', ' ').title()}:"),
                dcc.Dropdown(
                    id={'type': 'input-field', 'name': col_name},
                    options=dropdown_options,
                    placeholder=f"Select {col_name.replace('_', ' ')}..."
                ),
                html.Button(
                    f"Go to {ref_table.replace('_', ' ').title()}",
                    id={'type': 'fk-navigate', 'name': col_name, 'target': ref_table},
                    style={'marginLeft': '10px', 'fontSize': 'small'}
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'})

        else:
            # For regular columns, create appropriate input fields based on data type
            input_type = col_type_to_input_type.get(col_type, 'text')
            
            input_field = html.Div([
                html.Label(f"{col_name.replace('_', ' ').title()}:"),
                dcc.Input(
                    id={'type': 'input-field', 'name': col_name},
                    type=input_type,
                    placeholder=f"Enter {col_name.replace('_', ' ')}..."
                )
            ], style={'marginBottom': '10px'})

        input_fields.append(input_field)

    # Build the entire tab content
    tab_content = html.Div([
        html.H2(f"{tab.replace('_', ' ').title()} Management"),

        html.Div(id={'type': 'output-message', 'table': tab},
                 style={'color': 'red', 'padding': '10px'}),

        dash_table.DataTable(
            id={'type': 'data-table', 'table': tab},
            columns=columns,
            row_selectable='single',
            selected_rows=[],
            page_action='native',
            page_size=10,
            style_table={'overflowX': 'auto'},
        ),
        html.Br(),

        html.Div(input_fields, style={'padding': '10px'}),

        html.Div([
            html.Button('Create', id={'type': 'create-button', 'table': tab}, n_clicks=0),
            html.Button('Update', id={'type': 'update-button', 'table': tab}, n_clicks=0,
                        style={'marginLeft': '10px'}),
            html.Button('Delete', id={'type': 'delete-button', 'table': tab}, n_clicks=0,
                        style={'marginLeft': '10px'}),
            html.Button('Clear', id={'type': 'clear-button', 'table': tab}, n_clicks=0,
                        style={'marginLeft': '10px'}),
        ], style={'padding': '10px'}),

        # Store the primary key information
        dcc.Store(id={'type': 'primary-key-info', 'table': tab},
                  data=[col['name'] for col in schema if col['pk']])
    ])

    return tab_content

# --- Callbacks for refreshing data tables ---
@app.callback(
    Output({'type': 'data-table', 'table': ALL}, 'data'),
    Input({'type': 'output-message', 'table': ALL}, 'children'),
    State({'type': 'data-table', 'table': ALL}, 'id')
)
def refresh_tables(_, table_ids):
    """Refreshes all data tables when CRUD operations are performed."""
    return [get_table_data_with_fk_descriptions(table_id['table']) for table_id in table_ids]

# --- Callback for displaying selected data in input fields ---
@app.callback(
    Output({'type': 'input-field', 'name': ALL}, 'value'),
    Input({'type': 'data-table', 'table': ALL}, 'selected_rows'),
    State({'type': 'data-table', 'table': ALL}, 'data'),
    State({'type': 'data-table', 'table': ALL}, 'id'),
    State({'type': 'input-field', 'name': ALL}, 'id')
)
def display_selected_data(selected_rows_list, data_list, table_ids, input_ids):
    """Fills the input fields with the data from the selected row."""
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # Find which table triggered the callback
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    trigger_dict = eval(trigger)    #pylint: disable=eval-used
    triggered_table = trigger_dict['table']

    # Find the index of the triggered table
    table_index = None
    for i, table_id in enumerate(table_ids):
        if table_id['table'] == triggered_table:
            table_index = i
            break

    if table_index is None or not selected_rows_list[table_index]:
        return [''] * len(input_ids)

    # Get the selected row data
    selected_row = data_list[table_index][selected_rows_list[table_index][0]]

    # Map the data to the input fields
    result = []
    for input_id in input_ids:
        col_name = input_id['name']
        if col_name in selected_row:
            result.append(selected_row[col_name])
        else:
            result.append('')

    return result

# --- Callback for navigating to foreign key tables ---
@app.callback(
    Output('tabs', 'value'),
    Input({'type': 'fk-navigate', 'name': ALL, 'target': ALL}, 'n_clicks'),
    State({'type': 'fk-navigate', 'name': ALL, 'target': ALL}, 'id'),
    prevent_initial_call=True
)
def navigate_to_fk_table(n_clicks_list, _button_ids):
    """Navigates to the tab for the referenced foreign key table."""
    ctx = dash.callback_context
    if not ctx.triggered or not any(n_clicks_list):
        raise PreventUpdate

    # Find which button was clicked
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    trigger_dict = eval(trigger)    #pylint: disable=eval-used

    # Get the target table
    target_table = trigger_dict['target']
    return target_table

# --- Callback for clearing input fields ---
@app.callback(
    Output({'type': 'input-field', 'name': ALL},
           'value',
           allow_duplicate=True
           ),
    Input({'type': 'clear-button', 'table': ALL}, 'n_clicks'),
    State({'type': 'clear-button', 'table': ALL}, 'id'),
    State({'type': 'input-field', 'name': ALL}, 'id'),
    prevent_initial_call=True
)
def clear_input_fields(n_clicks_list, _button_ids, input_ids):
    """Clears all input fields when the Clear button is clicked."""
    ctx = dash.callback_context
    if not ctx.triggered or not any(n_clicks_list):
        raise PreventUpdate

    return [''] * len(input_ids)

# --- CRUD operation callbacks ---

# Create operation
@app.callback(
    Output({'type': 'output-message', 'table': ALL},
           'children',
           allow_duplicate=True
           ),
    Input({'type': 'create-button', 'table': ALL}, 'n_clicks'),
    State({'type': 'input-field', 'name': ALL}, 'value'),
    State({'type': 'input-field', 'name': ALL}, 'id'),
    State({'type': 'create-button', 'table': ALL}, 'id'),
    prevent_initial_call=True
)
def create_entry(n_clicks_list, input_values, input_ids, button_ids):
    """Creates a new entry in the selected table."""
    ctx = dash.callback_context
    if not ctx.triggered or not any(n_clicks_list):
        raise PreventUpdate

    # Find which button was clicked
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    trigger_dict = eval(trigger)    #pylint: disable=eval-used
    triggered_table = trigger_dict['table']

    # Get the column names and values
    columns = []
    values = []
    for i, input_id in enumerate(input_ids):
        if input_values[i]:  # Only include non-empty fields
            columns.append(input_id['name'])
            values.append(input_values[i])

    if not columns:
        return ["Please provide at least one value for creating a new entry."] * len(button_ids)

    # Build the SQL query
    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)
    query = f"INSERT INTO {triggered_table} ({columns_str}) VALUES ({placeholders})"

    conn = get_db_connection()
    try:
        with conn:
            conn.execute(query, values)

        # Create a result list
        # with success message for the triggered table
        # and empty strings for others
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"New entry created successfully in {triggered_table}.")
            else:
                result.append("")

        return result
    except sqlite3.IntegrityError as e:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"Error: {e}")
            else:
                result.append("")
        return result
    except sqlite3.Error as e:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"Database error: {e}")
            else:
                result.append("")
        return result
    finally:
        conn.close()

# Update operation
@app.callback(
    Output({'type': 'output-message', 'table': ALL},
           'children',
           allow_duplicate=True
           ),
    Input({'type': 'update-button', 'table': ALL}, 'n_clicks'),
    State({'type': 'input-field', 'name': ALL}, 'value'),
    State({'type': 'input-field', 'name': ALL}, 'id'),
    State({'type': 'update-button', 'table': ALL}, 'id'),
    State({'type': 'data-table', 'table': ALL}, 'selected_rows'),
    State({'type': 'data-table', 'table': ALL}, 'data'),
    State({'type': 'primary-key-info', 'table': ALL}, 'data'),
    prevent_initial_call=True
)
def update_entry(n_clicks_list, input_values, input_ids, button_ids, selected_rows_list,
                data_list, primary_key_info_list):
    """Updates an existing entry in the selected table."""
    ctx = dash.callback_context
    if not ctx.triggered or not any(n_clicks_list):
        raise PreventUpdate

    # Find which button was clicked
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    trigger_dict = eval(trigger)    #pylint: disable=eval-used
    triggered_table = trigger_dict['table']

    # Find the index of the triggered table
    table_index = None
    for i, button_id in enumerate(button_ids):
        if button_id['table'] == triggered_table:
            table_index = i
            break

    if table_index is None or not selected_rows_list[table_index]:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append("Please select a row to update.")
            else:
                result.append("")
        return result

    # Get the selected row and primary key info
    selected_row = data_list[table_index][selected_rows_list[table_index][0]]
    primary_keys = primary_key_info_list[table_index]

    # Get the column names and values to update
    set_clauses = []
    update_values = []
    for i, input_id in enumerate(input_ids):
        col_name = input_id['name']
        if input_values[i] is not None and input_values[i] != '':
            set_clauses.append(f"{col_name} = ?")
            update_values.append(input_values[i])

    if not set_clauses:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append("Please provide at least one value to update.")
            else:
                result.append("")
        return result

    # Build the WHERE clause for the primary keys
    where_clauses = []
    for pk in primary_keys:
        where_clauses.append(f"{pk} = ?")
        update_values.append(selected_row[pk])

    # Build the SQL query
    set_str = ', '.join(set_clauses)
    where_str = ' AND '.join(where_clauses)
    query = f"UPDATE {triggered_table} SET {set_str} WHERE {where_str}"

    conn = get_db_connection()
    try:
        with conn:
            conn.execute(query, update_values)

        # Create a result list
        # with success message for the triggered table
        # and empty strings for others
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"Entry updated successfully in {triggered_table}.")
            else:
                result.append("")

        return result
    except sqlite3.IntegrityError as e:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"Error: {e}")
            else:
                result.append("")
        return result
    except sqlite3.Error as e:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"Database error: {e}")
            else:
                result.append("")
        return result
    finally:
        conn.close()

# Delete operation
@app.callback(
    Output({'type': 'output-message', 'table': ALL},
           'children',
           allow_duplicate=True
           ),
    Input({'type': 'delete-button', 'table': ALL}, 'n_clicks'),
    State({'type': 'delete-button', 'table': ALL}, 'id'),
    State({'type': 'data-table', 'table': ALL}, 'selected_rows'),
    State({'type': 'data-table', 'table': ALL}, 'data'),
    State({'type': 'primary-key-info', 'table': ALL}, 'data'),
    prevent_initial_call=True
)
def delete_entry(n_clicks_list, button_ids, selected_rows_list, data_list, primary_key_info_list):
    """Deletes an entry from the selected table."""
    #pylint: disable=too-many-branches
    ctx = dash.callback_context
    if not ctx.triggered or not any(n_clicks_list):
        raise PreventUpdate

    # Find which button was clicked
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    trigger_dict = eval(trigger)  #pylint: disable=eval-used
    triggered_table = trigger_dict['table']

    # Find the index of the triggered table
    table_index = None
    for i, button_id in enumerate(button_ids):
        if button_id['table'] == triggered_table:
            table_index = i
            break

    if table_index is None or not selected_rows_list[table_index]:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append("Please select a row to delete.")
            else:
                result.append("")
        return result

    # Get the selected row and primary key info
    selected_row = data_list[table_index][selected_rows_list[table_index][0]]
    primary_keys = primary_key_info_list[table_index]

    # Build the WHERE clause for the primary keys
    where_clauses = []
    delete_values = []
    for pk in primary_keys:
        where_clauses.append(f"{pk} = ?")
        delete_values.append(selected_row[pk])

    # Build the SQL query
    where_str = ' AND '.join(where_clauses)
    query = f"DELETE FROM {triggered_table} WHERE {where_str}"

    conn = get_db_connection()
    try:
        with conn:
            conn.execute(query, delete_values)

        # Create a result list with success message for the triggered table
        # and empty strings for others
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"Entry deleted successfully from {triggered_table}.")
            else:
                result.append("")

        return result
    except sqlite3.IntegrityError as e:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"Error: This record cannot be deleted"
                              f" due to foreign key constraints. {e}"
                              )
            else:
                result.append("")
        return result
    except sqlite3.Error as e:
        result = []
        for button_id in button_ids:
            if button_id['table'] == triggered_table:
                result.append(f"Database error: {e}")
            else:
                result.append("")
        return result
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
