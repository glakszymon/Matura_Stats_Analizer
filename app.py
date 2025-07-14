import dash
from dash import dcc, html, Input, Output, State, ALL
from theme import LIGHT_THEME
from layouts import get_sidebar, get_home_layout, get_stats_layout, get_stats_layout_it
from callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Custom CSS for enhanced styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            .sidebar-item:hover {
                background: rgba(255, 255, 255, 0.1) !important;
                transform: translateX(8px);
            }
            
            .task-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 20px 40px rgba(102, 126, 234, 0.25) !important;
            }
            
            .task-item:hover {
                transform: translateY(-4px);
                box-shadow: 0 15px 30px rgba(102, 126, 234, 0.2) !important;
            }
            
            .fab-button:hover {
                transform: scale(1.1);
                box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3) !important;
            }
            
            @keyframes floating {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
                100% { transform: translateY(0px); }
            }
            
            .floating {
                animation: floating 3s ease-in-out infinite;
            }
            
            /* Right side panel animation */
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
            
            .slide-panel {
                animation: slideInRight 0.3s ease-out;
            }
            
            .slide-panel.closing {
                animation: slideOutRight 0.3s ease-in;
            }
            
            /* Overlay for side panel */
            .panel-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.4);
                backdrop-filter: blur(3px);
                z-index: 9999;
                opacity: 0;
                animation: fadeIn 0.3s ease-out forwards;
            }
            
            @keyframes fadeIn {
                to { opacity: 1; }
            }
            
            /* Side panel styling */
            .side-panel {
                position: fixed;
                top: 0;
                right: 0;
                width: 500px;
                height: 100vh;
                background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
                backdrop-filter: blur(20px);
                border-left: 1px solid rgba(255, 255, 255, 0.3);
                box-shadow: -10px 0 40px rgba(0, 0, 0, 0.1);
                z-index: 10000;
                overflow-y: auto;
                padding: 0;
            }
            
            @media (max-width: 768px) {
                .side-panel {
                    width: 100vw;
                    right: 0;
                }
            }
            
            /* Modal overlay that allows scrolling */
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(5px);
                z-index: 10000;
                overflow-y: auto;
                padding: 20px;
            }
            
            .modal-content {
                min-height: 100vh;
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding: 40px 0;
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
            }
            
            /* Button hover effects */
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
            }
            
            /* Glass morphism effect */
            .glass {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            /* Smooth transitions */
            * {
                transition: all 0.3s ease;
            }
            
            /* Fix for gradient text headers */
            .gradient-text {
                -webkit-text-fill-color: white;
                color: white;
            }
            
            .panel-content {
                padding: 24px;
                height: calc(100vh - 100px);
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    get_sidebar(),
    
    # Right side panel for adding tasks
    html.Div(
        id='add-set-modal',
        children=[
            # Overlay
            html.Div(
                id='panel-overlay',
                className='panel-overlay',
                style={'display': 'none'}
            ),
            # Side panel
            html.Div([

                # Panel header - bez formatowania
                html.Div([
                    html.Div([
                        html.H2([
                            html.Span("✨", style={'marginRight': '12px'}),
                            "Dodaj nowy zestaw"
                        ], style={
                            'color': LIGHT_THEME['text'],
                            'fontWeight': '800',
                            'fontSize': '24px',
                            'margin': '0'
                        }),
                        html.Button([
                            html.Span("✕", style={'fontSize': '20px'})
                        ],
                            id='close-add-set-modal',
                            n_clicks=0,
                            style={
                                'position': 'absolute',
                                'top': '20px',
                                'right': '20px',
                                'width': '40px',
                                'height': '40px',
                                'borderRadius': '50%',
                                'background': 'rgba(0, 0, 0, 0.1)',
                                'color': '#333',
                                'border': 'none',
                                'cursor': 'pointer',
                                'fontSize': '18px',
                                'fontWeight': 'bold',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'transition': 'all 0.3s ease'
                            }
                        )
                    ], style={'position': 'relative', 'padding': '24px'})
                ]),
                
                # Panel content
                html.Div([
                    html.Div([
                        html.Label("📚 Przedmiot:", style={
                            'display': 'block',
                            'marginBottom': '8px',
                            'fontWeight': '700',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '16px'
                        }),
                        dcc.Dropdown(
                            id='subject-dropdown',
                            options=[
                                {'label': '📊 Matematyka', 'value': 'matematyka'},
                                {'label': '💻 Informatyka', 'value': 'informatyka'}
                            ],
                            value='matematyka',
                            style={
                                'width': '100%',
                                'marginBottom': '24px',
                                'borderRadius': LIGHT_THEME['radius'],
                                'fontSize': '16px'
                            }
                        ),
                        
                        html.Label("📝 Nazwa zestawu:", style={
                            'display': 'block',
                            'marginBottom': '8px',
                            'fontWeight': '700',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '16px'
                        }),
                        dcc.Input(
                            id='task-set-name',
                            type='text',
                            placeholder='Np. "Próbna matura 2023"',
                            style={
                                'width': '100%',
                                'padding': '14px',
                                'border': f"2px solid {LIGHT_THEME['border']}",
                                'borderRadius': LIGHT_THEME['radius'],
                                'fontSize': '16px',
                                'marginBottom': '24px',
                                'background': LIGHT_THEME['input_bg'],
                                'fontWeight': '500',
                                'transition': 'all 0.3s ease'
                            }
                        ),
                        
                        html.Label("🔢 Liczba zadań:", style={
                            'display': 'block',
                            'marginBottom': '8px',
                            'fontWeight': '700',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '16px'
                        }),
                        html.Div([
                            dcc.Input(
                                id='task-set-size',
                                type='number',
                                min=1,
                                max=20,
                                value=5,
                                style={
                                    'width': '80px',
                                    'padding': '14px',
                                    'border': f"2px solid {LIGHT_THEME['border']}",
                                    'borderRadius': LIGHT_THEME['radius'],
                                    'fontSize': '16px',
                                    'background': LIGHT_THEME['input_bg'],
                                    'fontWeight': '600',
                                    'textAlign': 'center'
                                }
                            ),
                            html.Button([
                                html.Span("⚡", style={'marginRight': '8px'}),
                                'Generuj'
                            ],
                                id='generate-task-form-button',
                                n_clicks=0,
                                style={
                                    'marginLeft': '12px',
                                    'padding': '14px 20px',
                                    'background': LIGHT_THEME['gradient_primary'],
                                    'color': 'white',
                                    'border': 'none',
                                    'borderRadius': LIGHT_THEME['radius'],
                                    'cursor': 'pointer',
                                    'fontWeight': '700',
                                    'fontSize': '14px',
                                    'boxShadow': LIGHT_THEME['shadow'],
                                    'transition': 'all 0.3s ease',
                                    'flex': '1'
                                }
                            )
                        ], style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'marginBottom': '24px'
                        }),
                        
                        html.Div(style={
                            'height': '2px',
                            'background': f"linear-gradient(90deg, {LIGHT_THEME['gradient_primary']}, transparent)",
                            'marginBottom': '24px',
                            'borderRadius': '1px'
                        }),
                        
                        html.Div(id='task-set-form-container', style={
                            'marginBottom': '24px'
                        }),
                        
                        html.Div(id='task-set-message', style={
                            'marginBottom': '20px',
                            'textAlign': 'center',
                            'fontSize': '16px',
                            'fontWeight': '600'
                        }),
                        
                        html.Div([
                            html.Button([
                                html.Span("💾", style={'marginRight': '8px'}),
                                'Zapisz zestaw'
                            ],
                                id='save-task-set-button',
                                n_clicks=0,
                                disabled=True,
                                style={
                                    'width': '100%',
                                    'padding': '16px',
                                    'background': LIGHT_THEME['button_success'],
                                    'color': 'white',
                                    'border': 'none',
                                    'borderRadius': LIGHT_THEME['radius'],
                                    'cursor': 'pointer',
                                    'fontWeight': '700',
                                    'fontSize': '16px',
                                    'boxShadow': LIGHT_THEME['shadow_strong'],
                                    'marginBottom': '12px'
                                }
                            )
                        ])
                    ])
                ], className='panel-content')
            ], className='side-panel slide-panel')
        ],
        style={'display': 'none'}
    ),
    
    # Edit modal (keeping as center modal)
    html.Div(
        id='edit-modal',
        children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("✏️ Edytuj zadanie", style={
                            'marginBottom': '24px',
                            'fontWeight': '800',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '24px',
                            'textAlign': 'center'
                        }),
                        html.Div(style={
                            'height': '3px',
                            'background': LIGHT_THEME['warning'],
                            'borderRadius': '2px',
                            'marginBottom': '24px'
                        })
                    ]),
                    
                    html.Label("📝 Nazwa zadania:", style={
                        'display': 'block',
                        'marginBottom': '8px',
                        'fontWeight': '700',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '16px'
                    }),
                    dcc.Input(
                        id='edit-task-name',
                        type='text',
                        style={
                            'width': '100%',
                            'padding': '14px',
                            'border': f"2px solid {LIGHT_THEME['border']}",
                            'borderRadius': LIGHT_THEME['radius'],
                            'fontSize': '16px',
                            'marginBottom': '20px',
                            'background': LIGHT_THEME['input_bg'],
                            'fontWeight': '500'
                        }
                    ),
                    
                    html.Label("📄 Treść zadania:", style={
                        'display': 'block',
                        'marginBottom': '8px',
                        'fontWeight': '700',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '16px'
                    }),
                    dcc.Textarea(
                        id='edit-task-content',
                        style={
                            'width': '100%',
                            'padding': '14px',
                            'border': f"2px solid {LIGHT_THEME['border']}",
                            'borderRadius': LIGHT_THEME['radius'],
                            'fontSize': '16px',
                            'minHeight': '120px',
                            'marginBottom': '20px',
                            'background': LIGHT_THEME['input_bg'],
                            'fontWeight': '500',
                            'resize': 'vertical'
                        }
                    ),
                    
                    html.Label("🏷️ Tagi:", style={
                        'display': 'block',
                        'marginBottom': '8px',
                        'fontWeight': '700',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '16px'
                    }),
                    dcc.Dropdown(
                        id='edit-task-tags',
                        multi=True,
                        style={
                            'width': '100%',
                            'marginBottom': '20px',
                            'borderRadius': LIGHT_THEME['radius']
                        }
                    ),
                    
                    html.Label("✅ Status zadania:", style={
                        'display': 'block',
                        'marginBottom': '8px',
                        'fontWeight': '700',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '16px'
                    }),
                    dcc.RadioItems(
                        id='edit-task-solved',
                        options=[
                            {'label': ' ❌ Nierozwiązane', 'value': False},
                            {'label': ' ✅ Rozwiązane poprawnie', 'value': True}
                        ],
                        value=False,
                        style={
                            'marginBottom': '24px',
                            'fontSize': '16px',
                            'fontWeight': '600'
                        }
                    ),
                    
                    html.Div([
                        html.Button([
                            html.Span("💾", style={'marginRight': '8px'}),
                            'Zapisz zmiany'
                        ],
                        id='save-edit-button',
                        n_clicks=0,
                        style={
                            'padding': '16px 36px',
                            'background': LIGHT_THEME['success'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': LIGHT_THEME['radius'],
                            'cursor': 'pointer',
                            'fontWeight': '700',
                            'fontSize': '16px',
                            'boxShadow': LIGHT_THEME['shadow'],
                            'marginRight': '16px'
                        }),
                        html.Button([
                            html.Span("❌", style={'marginRight': '8px'}),
                            'Anuluj'
                        ],
                        id='cancel-edit-button',
                        n_clicks=0,
                        style={
                            'padding': '16px 36px',
                            'background': LIGHT_THEME['placeholder'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': LIGHT_THEME['radius'],
                            'cursor': 'pointer',
                            'fontWeight': '700',
                            'fontSize': '16px',
                            'boxShadow': LIGHT_THEME['shadow']
                        })
                    ], style={'textAlign': 'center'})
                ], style={
                    'background': LIGHT_THEME['content_bg'],
                    'padding': '40px',
                    'borderRadius': LIGHT_THEME['radius'],
                    'maxWidth': '600px',
                    'width': '90%',
                    'boxShadow': LIGHT_THEME['shadow'],
                    'backdropFilter': 'blur(20px)',
                    'border': f"1px solid {LIGHT_THEME['border']}",
                    'margin': '0 auto'
                })
            ], className='modal-content')
        ],
        className='modal-overlay',
        style={'display': 'none'}
    ),
    
    html.Div(
        id='page-content',
        style={
            'marginLeft': '280px',
            'padding': '0',
            'background': 'transparent',
            'minHeight': '100vh',
            'fontFamily': LIGHT_THEME['font']
        }
    ),
    dcc.Store(id='math-tasks-store', data=[]),
    dcc.Store(id='task-set-store', data={'tasks': [], 'current_set': None, 'subject': 'matematyka'}),
    dcc.Store(id='edit-task-store', data={}),
])

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)