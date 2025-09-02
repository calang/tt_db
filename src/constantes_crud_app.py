#!/usr/bin/env python3

"""CRUD for constantes table"""

import os
import sqlite3

import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd

# --- Database setup ---
DB_FILE = 'data/tt.db'

def get_db_connection():
    """Establishes connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the 'constantes' table if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        print(f"Creating database {DB_FILE}...")
        conn = get_db_connection()
        try:
            with conn:
                conn.execute('''
                    CREATE TABLE constantes (
                        name TEXT NOT NULL PRIMARY KEY,
                        value INTEGER NOT NULL
                    )
                ''')
            print("Table 'constantes' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

# Initialize the database
init_db()

# --- Dash App ---
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# --- App Layout ---
app.layout = html.Div([
    html.H1('Constantes CRUD Operations'),

    html.Div(id='output-message', style={'color': 'red', 'padding': '10px'}),

    dash_table.DataTable(
        id='constantes-table',
        columns=[
            {'name': 'Name', 'id': 'name'},
            {'name': 'Value', 'id': 'value'}
        ],
        row_selectable='single',
        selected_rows=[],
        page_action='native',
        page_size=10,
    ),
    html.Br(),

    html.Div([
        dcc.Input(id='input-name', type='text', placeholder='Enter Name...'),
        dcc.Input(id='input-value', type='number', placeholder='Enter Value...'),
    ], style={'padding': '10px'}),

    html.Div([
        html.Button('Create', id='create-button', n_clicks=0),
        html.Button('Update', id='update-button', n_clicks=0),
        html.Button('Delete', id='delete-button', n_clicks=0),
    ], style={'padding': '10px'})
])

# --- Callbacks ---

@app.callback(
    Output('constantes-table', 'data'),
    Input('output-message', 'children')
)
def refresh_table(_):
    """Refreshes the data table whenever a CRUD operation is performed."""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM constantes", conn)
        return df.to_dict('records')
    finally:
        conn.close()

@app.callback(
    [Output('input-name', 'value'), Output('input-value', 'value')],
    Input('constantes-table', 'selected_rows'),
    State('constantes-table', 'data')
)
def display_selected_data(selected_rows, data):
    """Fills the input fields with the data from the selected row."""
    if selected_rows:
        selected_row = data[selected_rows[0]]
        return selected_row['name'], selected_row['value']
    return '', ''

@app.callback(
    Output('output-message', 'children', allow_duplicate=True),
    Input('create-button', 'n_clicks'),
    State('input-name', 'value'),
    State('input-value', 'value'),
    prevent_initial_call='initial_duplicate'
)
def create_entry(n_clicks, name, value):
    """Creates a new entry in the 'constantes' table."""
    if n_clicks > 0 and name and value is not None:
        conn = get_db_connection()
        try:
            with conn:
                conn.execute("INSERT INTO constantes (name, value) VALUES (?, ?)", (name, value))
            return f"'{name}' created successfully."
        except sqlite3.IntegrityError:
            return f"Error: An entry with the name '{name}' already exists."
        except sqlite3.Error as e:
            return f"Database error: {e}"
        finally:
            conn.close()
    return ""

@app.callback(
    Output('output-message', 'children', allow_duplicate=True),
    Input('update-button', 'n_clicks'),
    State('input-name', 'value'),
    State('input-value', 'value'),
    State('constantes-table', 'selected_rows'),
    State('constantes-table', 'data'),
    prevent_initial_call='initial_duplicate'
)
def update_entry(n_clicks, name, value, selected_rows, data):
    """Updates an existing entry in the 'constantes' table."""
    if n_clicks > 0 and selected_rows:
        if name and value is not None:
            original_name = data[selected_rows[0]]['name']
            conn = get_db_connection()
            try:
                with conn:
                    conn.execute("UPDATE constantes SET name = ?,"
                                 "value = ? WHERE name = ?",
                                 (name, value, original_name)
                                 )
                return f"'{original_name}' updated successfully."
            except sqlite3.IntegrityError:
                return f"Error: An entry with the name '{name}' already exists."
            except sqlite3.Error as e:
                return f"Database error: {e}"
            finally:
                conn.close()
        else:
            return "Please provide both name and value for updating."
    return ""

@app.callback(
    Output('output-message', 'children', allow_duplicate=True),
    Input('delete-button', 'n_clicks'),
    State('constantes-table', 'selected_rows'),
    State('constantes-table', 'data'),
    prevent_initial_call='initial_duplicate'
)
def delete_entry(n_clicks, selected_rows, data):
    """Deletes an entry from the 'constantes' table."""
    if n_clicks > 0 and selected_rows:
        name_to_delete = data[selected_rows[0]]['name']
        conn = get_db_connection()
        try:
            with conn:
                conn.execute("DELETE FROM constantes WHERE name = ?", (name_to_delete,))
            return f"'{name_to_delete}' deleted successfully."
        except sqlite3.Error as e:
            return f"Database error: {e}"
        finally:
            conn.close()
    return ""

if __name__ == '__main__':
    app.run(debug=True)
