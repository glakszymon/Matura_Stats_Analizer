import dash
from dash import dcc, html, Input, Output, State, ALL
from theme import LIGHT_THEME
from layouts import get_sidebar, get_home_layout, get_stats_layout, get_stats_layout_it, get_stats_layout_polski, get_stats_layout_angielski, get_manage_categories_layout, get_settings_layout
from callbacks import register_callbacks
from template_loader import load_html_template

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Load HTML template from external file
html_template = load_html_template()
if html_template:
    app.index_string = html_template
else:
    # Fallback to basic template if loading fails
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>Matura Dashboard</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            <button class="mobile-menu-btn" id="mobile-menu-toggle">☰</button>
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
    
    # Mobile menu overlay
    html.Div(
        id='mobile-menu-overlay',
        style={
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'right': 0,
            'bottom': 0,
            'background': 'rgba(0,0,0,0.5)',
            'zIndex': 1000,  # Pod sidebar (1001)
            'display': 'none'
        }
    ),
    
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
                # Panel header
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
                                {'label': '∑ Matematyka', 'value': 'matematyka'},
                                {'label': '💻 Informatyka', 'value': 'informatyka'},
                                {'label': '🇵🇱 Język Polski', 'value': 'polski'},
                                {'label': '🇬🇧 Język Angielski', 'value': 'angielski'}
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
    
    # Edit set modal
    html.Div(
        id='edit-set-modal',
        children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("✏️ Edytuj zestaw", style={
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
                    
                    html.Label("📝 Nazwa zestawu:", style={
                        'display': 'block',
                        'marginBottom': '8px',
                        'fontWeight': '700',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '16px'
                    }),
                    dcc.Input(
                        id='edit-set-name',
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
                    
                    html.Label("📚 Przedmiot:", style={
                        'display': 'block',
                        'marginBottom': '8px',
                        'fontWeight': '700',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '16px'
                    }),
                    dcc.Dropdown(
                        id='edit-set-subject',
                        options=[
                            {'label': '∑ Matematyka', 'value': 'matematyka'},
                            {'label': '💻 Informatyka', 'value': 'informatyka'},
                            {'label': '🇵🇱 Język Polski', 'value': 'polski'},
                            {'label': '🇬🇧 Język Angielski', 'value': 'angielski'}
                        ],
                        style={
                            'width': '100%',
                            'marginBottom': '24px',
                            'borderRadius': LIGHT_THEME['radius'],
                            'fontSize': '16px'
                        }
                    ),
                    
                    html.Div([
                        html.Button([
                            html.Span("💾", style={'marginRight': '8px'}),
                            'Zapisz zmiany'
                        ],
                        id='save-edit-set-button',
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
                        id='cancel-edit-set-button',
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
                    'maxWidth': '500px',
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
    
    # Delete confirmation modal
    html.Div(
        id='delete-modal',
        children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.Div("⚠️", style={
                            'fontSize': '64px',
                            'textAlign': 'center',
                            'marginBottom': '20px',
                            'color': LIGHT_THEME['error']
                        }),
                        html.H3("Czy na pewno chcesz usunąć to zadanie?", style={
                            'marginBottom': '16px',
                            'fontWeight': '800',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '24px',
                            'textAlign': 'center'
                        }),
                        html.Div(style={
                            'height': '3px',
                            'background': LIGHT_THEME['error'],
                            'borderRadius': '2px',
                            'marginBottom': '24px'
                        })
                    ]),
                    
                    html.Div([
                        html.Div([
                            html.Strong("📝 Nazwa: ", style={'color': LIGHT_THEME['text']}),
                            html.Span(id='delete-task-name', style={'color': LIGHT_THEME['placeholder']})
                        ], style={'marginBottom': '12px', 'fontSize': '16px'}),
                        html.Div([
                            html.Strong("🏷️ Tagi: ", style={'color': LIGHT_THEME['text']}),
                            html.Span(id='delete-task-tags', style={'color': LIGHT_THEME['placeholder']})
                        ], style={'marginBottom': '12px', 'fontSize': '16px'}),
                        html.Div([
                            html.Strong("✅ Status: ", style={'color': LIGHT_THEME['text']}),
                            html.Span(id='delete-task-status', style={'color': LIGHT_THEME['placeholder']})
                        ], style={'marginBottom': '24px', 'fontSize': '16px'})
                    ], style={
                        'background': 'linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%)',
                        'padding': '20px',
                        'borderRadius': LIGHT_THEME['radius'],
                        'border': f"2px solid {LIGHT_THEME['error']}20",
                        'marginBottom': '24px'
                    }),
                    
                    html.P("Ta operacja jest nieodwracalna!", style={
                        'textAlign': 'center',
                        'color': LIGHT_THEME['error'],
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),
                    
                    html.Div([
                        html.Button([
                            html.Span("🗑️", style={'marginRight': '8px'}),
                            'Tak, usuń zadanie'
                        ],
                        id='confirm-delete-button',
                        n_clicks=0,
                        style={
                            'padding': '16px 36px',
                            'background': LIGHT_THEME['error'],
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
                        id='cancel-delete-button',
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
                    'maxWidth': '500px',
                    'width': '90%',
                    'boxShadow': LIGHT_THEME['shadow_strong'],
                    'backdropFilter': 'blur(20px)',
                    'border': f"1px solid {LIGHT_THEME['border']}",
                    'margin': '0 auto'
                })
            ], className='modal-content')
        ],
        className='modal-overlay',
        style={'display': 'none'}
    ),
    
    # Add task to set modal
    html.Div(
        id='add-task-to-set-modal',
        children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("➕ Dodaj zadanie do zestawu", style={
                            'marginBottom': '16px',
                            'fontWeight': '800',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '24px',
                            'textAlign': 'center'
                        }),
                        html.P(id='add-task-set-name-display', style={
                            'textAlign': 'center',
                            'color': LIGHT_THEME['placeholder'],
                            'fontSize': '16px',
                            'marginBottom': '24px',
                            'fontWeight': '500'
                        }),
                        html.Div(style={
                            'height': '3px',
                            'background': LIGHT_THEME['gradient_primary'],
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
                        id='add-task-name',
                        type='text',
                        placeholder='Nazwa zadania...',
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
                        id='add-task-content',
                        placeholder='Treść zadania...',
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
                        id='add-task-tags',
                        multi=True,
                        placeholder="Wybierz tagi...",
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
                        id='add-task-solved',
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
                            'Dodaj zadanie'
                        ],
                        id='save-add-task-button',
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
                        id='cancel-add-task-button',
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
    
    # Admin panel modal (hidden, activated by keyboard shortcut)
    html.Div(
        id='admin-panel-modal',
        children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("🔧 Panel Administratora", style={
                            'marginBottom': '24px',
                            'fontWeight': '800',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '24px',
                            'textAlign': 'center'
                        }),
                        html.P("Uwaga: Te operacje są nieodwracalne!", style={
                            'textAlign': 'center',
                            'color': LIGHT_THEME['error'],
                            'fontSize': '16px',
                            'fontWeight': '600',
                            'marginBottom': '24px'
                        }),
                        html.Div(style={
                            'height': '3px',
                            'background': LIGHT_THEME['error'],
                            'borderRadius': '2px',
                            'marginBottom': '24px'
                        })
                    ]),
                    
                    html.Div([
                        html.H4("🗑️ Czyszczenie Bazy Danych", style={
                            'color': LIGHT_THEME['text'],
                            'fontWeight': '700',
                            'fontSize': '18px',
                            'marginBottom': '16px'
                        }),
                        
                        html.Button([
                            html.Span("🏷️", style={'marginRight': '8px'}),
                            'Wyczyść Wszystkie Kategorie'
                        ],
                        id='admin-clear-categories-button',
                        n_clicks=0,
                        style={
                            'width': '100%',
                            'padding': '16px',
                            'background': LIGHT_THEME['warning'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': LIGHT_THEME['radius'],
                            'cursor': 'pointer',
                            'fontWeight': '700',
                            'fontSize': '16px',
                            'boxShadow': LIGHT_THEME['shadow'],
                            'marginBottom': '12px'
                        }),
                        
                        html.Button([
                            html.Span("📝", style={'marginRight': '8px'}),
                            'Wyczyść Wszystkie Zadania'
                        ],
                        id='admin-clear-tasks-button',
                        n_clicks=0,
                        style={
                            'width': '100%',
                            'padding': '16px',
                            'background': LIGHT_THEME['error'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': LIGHT_THEME['radius'],
                            'cursor': 'pointer',
                            'fontWeight': '700',
                            'fontSize': '16px',
                            'boxShadow': LIGHT_THEME['shadow'],
                            'marginBottom': '12px'
                        }),
                        
                        html.Button([
                            html.Span("💣", style={'marginRight': '8px'}),
                            'Wyczyść Całą Bazę Danych'
                        ],
                        id='admin-clear-all-button',
                        n_clicks=0,
                        style={
                            'width': '100%',
                            'padding': '16px',
                            'background': '#8b0000',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': LIGHT_THEME['radius'],
                            'cursor': 'pointer',
                            'fontWeight': '700',
                            'fontSize': '16px',
                            'boxShadow': LIGHT_THEME['shadow'],
                            'marginBottom': '24px'
                        })
                    ]),
                    
                    html.Div(id='admin-message', style={
                        'textAlign': 'center',
                        'marginBottom': '24px',
                        'fontSize': '16px',
                        'fontWeight': '600'
                    }),
                    
                    html.Div([
                        html.Button([
                            html.Span("❌", style={'marginRight': '8px'}),
                            'Zamknij'
                        ],
                        id='close-admin-panel-button',
                        n_clicks=0,
                        style={
                            'width': '100%',
                            'padding': '16px',
                            'background': LIGHT_THEME['placeholder'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': LIGHT_THEME['radius'],
                            'cursor': 'pointer',
                            'fontWeight': '700',
                            'fontSize': '16px',
                            'boxShadow': LIGHT_THEME['shadow']
                        })
                    ])
                ], style={
                    'background': LIGHT_THEME['content_bg'],
                    'padding': '40px',
                    'borderRadius': LIGHT_THEME['radius'],
                    'maxWidth': '500px',
                    'width': '90%',
                    'boxShadow': LIGHT_THEME['shadow_strong'],
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
            'fontFamily': LIGHT_THEME['font'],
            'transition': 'margin-left 0.3s ease'
        },
        className='page-content'
    ),
    dcc.Store(id='math-tasks-store', data=[]),
    dcc.Store(id='task-set-store', data={'tasks': [], 'current_set': None, 'subject': 'matematyka'}),
    dcc.Store(id='edit-task-store', data={}),
    dcc.Store(id='edit-set-store', data={}),
    dcc.Store(id='add-task-to-set-store', data={}),
    dcc.Store(id='delete-task-store', data={}),
    dcc.Store(id='keyboard-store', data={'keys': []}),
    dcc.Store(id='theme-store', data={'theme': 'light'}),
    
    # Confirmation modals for database operations
    html.Div(
        id='confirm-clear-categories-modal',
        children=[
            html.Div([
                html.Div([
                    html.Div("⚠️", style={
                        'fontSize': '64px',
                        'textAlign': 'center',
                        'marginBottom': '20px',
                        'color': LIGHT_THEME['warning']
                    }),
                    html.H3("Czy na pewno chcesz usunąć wszystkie kategorie?", style={
                        'marginBottom': '16px',
                        'fontWeight': '800',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '24px',
                        'textAlign': 'center'
                    }),
                    html.P("Ta operacja usunie wszystkie kategorie z bazy danych!", style={
                        'textAlign': 'center',
                        'color': LIGHT_THEME['error'],
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),
                    html.P("Ta operacja jest nieodwracalna!", style={
                        'textAlign': 'center',
                        'color': LIGHT_THEME['error'],
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),
                    
                    html.Div([
                        html.Button([
                            html.Span("🗑️", style={'marginRight': '8px'}),
                            'Tak, usuń wszystkie kategorie'
                        ],
                        id='confirm-clear-categories-button',
                        n_clicks=0,
                        style={
                            'padding': '16px 36px',
                            'background': LIGHT_THEME['warning'],
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
                        id='cancel-clear-categories-button',
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
                    'maxWidth': '500px',
                    'width': '90%',
                    'boxShadow': LIGHT_THEME['shadow_strong'],
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
        id='confirm-clear-tasks-modal',
        children=[
            html.Div([
                html.Div([
                    html.Div("⚠️", style={
                        'fontSize': '64px',
                        'textAlign': 'center',
                        'marginBottom': '20px',
                        'color': LIGHT_THEME['error']
                    }),
                    html.H3("Czy na pewno chcesz usunąć wszystkie zadania?", style={
                        'marginBottom': '16px',
                        'fontWeight': '800',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '24px',
                        'textAlign': 'center'
                    }),
                    html.P("Ta operacja usunie wszystkie zadania i zestawy z bazy danych!", style={
                        'textAlign': 'center',
                        'color': LIGHT_THEME['error'],
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),
                    html.P("Ta operacja jest nieodwracalna!", style={
                        'textAlign': 'center',
                        'color': LIGHT_THEME['error'],
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),
                    
                    html.Div([
                        html.Button([
                            html.Span("🗑️", style={'marginRight': '8px'}),
                            'Tak, usuń wszystkie zadania'
                        ],
                        id='confirm-clear-tasks-button',
                        n_clicks=0,
                        style={
                            'padding': '16px 36px',
                            'background': LIGHT_THEME['error'],
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
                        id='cancel-clear-tasks-button',
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
                    'maxWidth': '500px',
                    'width': '90%',
                    'boxShadow': LIGHT_THEME['shadow_strong'],
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
        id='confirm-clear-all-modal',
        children=[
            html.Div([
                html.Div([
                    html.Div("💣", style={
                        'fontSize': '64px',
                        'textAlign': 'center',
                        'marginBottom': '20px',
                        'color': '#8b0000'
                    }),
                    html.H3("OSTATECZNE OSTRZEŻENIE!", style={
                        'marginBottom': '16px',
                        'fontWeight': '800',
                        'color': LIGHT_THEME['text'],
                        'fontSize': '24px',
                        'textAlign': 'center'
                    }),
                    html.P("Ta operacja usunie CAŁĄ bazę danych - wszystkie zadania, zestawy i kategorie!", style={
                        'textAlign': 'center',
                        'color': '#8b0000',
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),
                    html.P("Ta operacja jest NIEODWRACALNA!", style={
                        'textAlign': 'center',
                        'color': '#8b0000',
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'marginBottom': '24px'
                    }),
                    
                    html.Div([
                        html.Button([
                            html.Span("💣", style={'marginRight': '8px'}),
                            'TAK, USUŃ WSZYSTKO'
                        ],
                        id='confirm-clear-all-button',
                        n_clicks=0,
                        style={
                            'padding': '16px 36px',
                            'background': '#8b0000',
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
                        id='cancel-clear-all-button',
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
                    'maxWidth': '500px',
                    'width': '90%',
                    'boxShadow': LIGHT_THEME['shadow_strong'],
                    'backdropFilter': 'blur(20px)',
                    'border': f"1px solid {LIGHT_THEME['border']}",
                    'margin': '0 auto'
                })
            ], className='modal-content')
        ],
        className='modal-overlay',
        style={'display': 'none'}
    ),
])

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
