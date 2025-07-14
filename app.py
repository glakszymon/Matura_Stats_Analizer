import dash
from dash import dcc, html, Input, Output, State, ALL
from theme import LIGHT_THEME
from layouts import get_sidebar, get_home_layout
from callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    get_sidebar(),
    html.Div(
        id='add-set-modal',
        children=[
            html.Div([
                html.H3("Dodaj nowy zestaw zadań", style={'marginBottom': '20px', 'fontWeight': 'bold'}),
                html.Label("Nazwa zestawu:", style={'display': 'block', 'marginBottom': '5px', 'fontWeight': 'bold'}),
                dcc.Input(
                    id='task-set-name',
                    type='text',
                    placeholder='Np. "Próbna matura 2023"',
                    style={
                        'width': '100%',
                        'padding': '12px',
                        'border': f"1.5px solid {LIGHT_THEME['border']}",
                        'borderRadius': LIGHT_THEME['radius'],
                        'fontSize': '17px',
                        'marginBottom': '15px',
                        'background': LIGHT_THEME['input_bg']
                    }
                ),
                html.Label("Liczba zadań w zestawie:", style={'display': 'block', 'marginBottom': '5px', 'fontWeight': 'bold'}),
                dcc.Input(
                    id='task-set-size',
                    type='number',
                    min=1,
                    max=20,
                    value=5,
                    style={
                        'width': '100px',
                        'padding': '12px',
                        'border': f"1.5px solid {LIGHT_THEME['border']}",
                        'borderRadius': LIGHT_THEME['radius'],
                        'fontSize': '17px',
                        'background': LIGHT_THEME['input_bg']
                    }
                ),
                html.Button(
                    'Generuj formularz',
                    id='generate-task-form-button',
                    n_clicks=0,
                    style={
                        'marginLeft': '15px',
                        'padding': '12px 24px',
                        'background': LIGHT_THEME['button_primary'],
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': LIGHT_THEME['radius'],
                        'cursor': 'pointer',
                        'fontWeight': 'bold',
                        'fontSize': '17px',
                        'boxShadow': LIGHT_THEME['shadow']
                    }
                ),
                html.Div(id='task-set-form-container', style={'marginBottom': '30px'}),
                html.Button(
                    'Zapisz zestaw zadań',
                    id='save-task-set-button',
                    n_clicks=0,
                    disabled=True,
                    style={
                        'padding': '14px 32px',
                        'background': LIGHT_THEME['success'],
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': LIGHT_THEME['radius'],
                        'cursor': 'pointer',
                        'fontWeight': 'bold',
                        'fontSize': '18px',
                        'display': 'block',
                        'margin': '0 auto',
                        'boxShadow': LIGHT_THEME['shadow']
                    }
                ),
                html.Button(
                    'Anuluj',
                    id='close-add-set-modal',
                    n_clicks=0,
                    style={
                        'padding': '12px 32px',
                        'background': LIGHT_THEME['placeholder'],
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': LIGHT_THEME['radius'],
                        'cursor': 'pointer',
                        'fontWeight': 'bold',
                        'fontSize': '16px',
                        'marginTop': '16px',
                    }
                ),
                html.Div(id='task-set-message', style={'marginTop': '15px', 'textAlign': 'center'})
            ], style={
                'background': LIGHT_THEME['content_bg'],
                'padding': '32px',
                'borderRadius': LIGHT_THEME['radius'],
                'maxWidth': '500px',
                'width': '90%',
                'boxShadow': LIGHT_THEME['shadow'],
                'position': 'relative',
            })
        ],
        style={
            'display': 'none',
            'position': 'absolute',
            'top': '60px',
            'left': '50%',
            'transform': 'translateX(-50%)',
            'width': '520px',
            'background': '#fff',
            'boxShadow': '0 4px 24px rgba(80, 112, 255, 0.10)',
            'borderRadius': '12px',
            'zIndex': 1000,
            'padding': '32px',
            'border': '1.5px solid #e0e0e0',
        }
    ),
    html.Div(
        id='page-content',
        style={
            'marginLeft': '260px',
            'padding': '40px 24px',
            'background': LIGHT_THEME['background'],
            'minHeight': '100vh',
            'fontFamily': LIGHT_THEME['font']
        }
    ),
    dcc.Store(id='math-tasks-store', data=[]),
    dcc.Store(id='task-set-store', data={'tasks': [], 'current_set': None}),
    dcc.Store(id='edit-task-store', data={}),
])

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)