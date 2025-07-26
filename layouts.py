# layouts.py
from dash import dcc, html
from theme import LIGHT_THEME, get_theme
# Usunięto import DEFAULT_CATEGORIES - nie są już używane

def get_sidebar():
    return html.Div([
        html.Div([
            # In get_sidebar() function, change line ~15:
            html.H2("📊 Matura Dashboard", style={
                'color': LIGHT_THEME['text_light'], 
                'padding': '32px 0 24px 0', 
                'fontWeight': '800', 
                'letterSpacing': '1px', 
                'textAlign': 'center',
                'fontSize': '28px',
                'margin': '0'
            }),

            html.Div(style={
                'height': '3px',
                'background': 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                'margin': '0 20px 30px 20px',
                'borderRadius': '2px'
            })
        ]),
        html.Ul([
            html.Li(
                dcc.Link([
                    html.Span("🏠", style={'marginRight': '12px', 'fontSize': '20px'}),
                    "Strona Główna"
                ], href="/", style={
                    'color': LIGHT_THEME['text_light'], 
                    'fontWeight': '600', 
                    'fontSize': '16px', 
                    'textDecoration': 'none', 
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                style={
                    'padding': '16px 24px', 
                    'borderBottom': '1px solid rgba(255,255,255,0.1)', 
                    'transition': 'all 0.3s ease',
                    'borderRadius': '12px',
                    'margin': '4px 12px'
                },
                className='sidebar-item'
            ),
            html.Li(
                dcc.Link([
                    html.Span("📚", style={'marginRight': '12px', 'fontSize': '20px'}),
                    "Zadania Maturalne"
                ], href="/math-tasks", style={
                    'color': LIGHT_THEME['text_light'], 
                    'fontWeight': '600', 
                    'fontSize': '16px', 
                    'textDecoration': 'none', 
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                style={
                    'padding': '16px 24px', 
                    'borderBottom': '1px solid rgba(255,255,255,0.1)', 
                    'transition': 'all 0.3s ease',
                    'borderRadius': '12px',
                    'margin': '4px 12px'
                },
                className='sidebar-item'
            ),
            html.Li(
                dcc.Link([
                    html.Span("∑", style={'marginRight': '12px', 'fontSize': '20px'}),
                    "Statystyki Matematyka"
                ], href="/stats", style={
                    'color': LIGHT_THEME['text_light'], 
                    'fontWeight': '600', 
                    'fontSize': '16px', 
                    'textDecoration': 'none', 
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                style={
                    'padding': '16px 24px', 
                    'borderBottom': '1px solid rgba(255,255,255,0.1)', 
                    'transition': 'all 0.3s ease',
                    'borderRadius': '12px',
                    'margin': '4px 12px'
                },
                className='sidebar-item'
            ),
            html.Li(
                dcc.Link([
                    html.Span("💻", style={'marginRight': '12px', 'fontSize': '20px'}),
                    "Statystyki Informatyka"
                ], href="/stats-it", style={
                    'color': LIGHT_THEME['text_light'], 
                    'fontWeight': '600', 
                    'fontSize': '16px', 
                    'textDecoration': 'none', 
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                style={
                    'padding': '16px 24px', 
                    'transition': 'all 0.3s ease',
                    'borderRadius': '12px',
                    'margin': '4px 12px'
                },
                className='sidebar-item'
            ),
            html.Li(
                dcc.Link([
                    html.Span("🇵🇱", style={'marginRight': '12px', 'fontSize': '20px'}),
                    "Statystyki Polski"
                ], href="/stats-polski", style={
                    'color': LIGHT_THEME['text_light'], 
                    'fontWeight': '600', 
                    'fontSize': '16px', 
                    'textDecoration': 'none', 
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                style={
                    'padding': '16px 24px', 
                    'transition': 'all 0.3s ease',
                    'borderRadius': '12px',
                    'margin': '4px 12px'
                },
                className='sidebar-item'
            ),
            html.Li(
                dcc.Link([
                    html.Span("🇬🇧", style={'marginRight': '12px', 'fontSize': '20px'}),
                    "Statystyki Angielski"
                ], href="/stats-angielski", style={
                    'color': LIGHT_THEME['text_light'], 
                    'fontWeight': '600', 
                    'fontSize': '16px', 
                    'textDecoration': 'none', 
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                style={
                    'padding': '16px 24px', 
                    'transition': 'all 0.3s ease',
                    'borderRadius': '12px',
                    'margin': '4px 12px'
                },
                className='sidebar-item'
            ),
            html.Li(
                dcc.Link([
                    html.Span("🏷️", style={'marginRight': '12px', 'fontSize': '20px'}),
                    "Zarządzaj Kategoriami"
                ], href="/manage-categories", style={
                    'color': LIGHT_THEME['text_light'], 
                    'fontWeight': '600', 
                    'fontSize': '16px', 
                    'textDecoration': 'none', 
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                style={
                    'padding': '16px 24px', 
                    'transition': 'all 0.3s ease',
                    'borderRadius': '12px',
                    'margin': '4px 12px'
                },
                className='sidebar-item'
            ),
            html.Li(
                dcc.Link([
                    html.Span("⚙️", style={'marginRight': '12px', 'fontSize': '20px'}),
                    "Ustawienia"
                ], href="/settings", style={
                    'color': LIGHT_THEME['text_light'], 
                    'fontWeight': '600', 
                    'fontSize': '16px', 
                    'textDecoration': 'none', 
                    'transition': 'all 0.3s ease',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                style={
                    'padding': '16px 24px', 
                    'transition': 'all 0.3s ease',
                    'borderRadius': '12px',
                    'margin': '4px 12px'
                },
                className='sidebar-item'
            ),
        ], style={'listStyleType': 'none', 'padding': 0, 'margin': 0}),
        
        # Footer in sidebar
        html.Div([
            html.P("Made with ❤️", style={
                'color': 'rgba(255,255,255,0.7)',
                'fontSize': '14px',
                'textAlign': 'center',
                'margin': '0'
            })
        ], style={
            'position': 'absolute',
            'bottom': '20px',
            'left': '0',
            'right': '0'
        })
    ], style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '280px',
        'background': LIGHT_THEME['sidebar_bg'],
        'boxShadow': LIGHT_THEME['shadow_strong'],
        'zIndex': 100,
        'borderTopRightRadius': LIGHT_THEME['radius_large'],
        'borderBottomRightRadius': LIGHT_THEME['radius_large'],
        'transition': 'transform 0.3s ease'
    }, className='sidebar')

def get_home_layout():
    return html.Div([
        html.Div([
            html.Div([
                html.Div("🎓", style={
                    'fontSize': '80px',
                    'textAlign': 'center',
                    'marginBottom': '24px',
                    'animation': 'floating 3s ease-in-out infinite'
                }),
                html.H1("Witaj w LifeChanger!", style={
                    'textAlign': 'center', 
                    'color': LIGHT_THEME['text'], 
                    'fontWeight': '800', 
                    'fontSize': 'clamp(32px, 5vw, 48px)',
                    'marginBottom': '20px'
                }),
                html.P("Zarządzaj zadaniami maturalnymi, śledź postępy i analizuj statystyki w nowoczesny sposób.", style={
                    'textAlign': 'center', 
                    'fontSize': 'clamp(16px, 2.5vw, 22px)', 
                    'color': LIGHT_THEME['text'], 
                    'marginTop': '20px',
                    'lineHeight': '1.6',
                    'fontWeight': '500'
                }),
                
                # Feature cards - now responsive
                html.Div([
                    html.Div([
                        html.Div("🇵🇱", style={'fontSize': '48px', 'marginBottom': '16px'}),
                        html.H3("Organizuj zadania", style={
                            'color': LIGHT_THEME['text'],
                            'fontWeight': '700',
                            'marginBottom': '12px',
                            'fontSize': 'clamp(18px, 2vw, 24px)'
                        }),
                        html.P("Twórz zestawy zadań maturalnych i organizuj je według przedmiotów", style={
                            'color': LIGHT_THEME['placeholder'],
                            'fontSize': 'clamp(14px, 1.5vw, 16px)',
                            'lineHeight': '1.5'
                        })
                    ], className='card', style={
                        'background': LIGHT_THEME['content_bg'],
                        'padding': 'clamp(20px, 3vw, 32px)',
                        'borderRadius': LIGHT_THEME['radius'],
                        'boxShadow': LIGHT_THEME['shadow'],
                        'textAlign': 'center',
                        'transition': 'transform 0.3s ease, box-shadow 0.3s ease'
                    }),
                    
                    html.Div([
                        html.Div("📊", style={'fontSize': '48px', 'marginBottom': '16px'}),
                        html.H3("Śledź postępy", style={
                            'color': LIGHT_THEME['text'],
                            'fontWeight': '700',
                            'marginBottom': '12px',
                            'fontSize': 'clamp(18px, 2vw, 24px)'
                        }),
                        html.P("Monitoruj swoje wyniki i identyfikuj obszary wymagające poprawy", style={
                            'color': LIGHT_THEME['placeholder'],
                            'fontSize': 'clamp(14px, 1.5vw, 16px)',
                            'lineHeight': '1.5'
                        })
                    ], className='card', style={
                        'background': LIGHT_THEME['content_bg'],
                        'padding': 'clamp(20px, 3vw, 32px)',
                        'borderRadius': LIGHT_THEME['radius'],
                        'boxShadow': LIGHT_THEME['shadow'],
                        'textAlign': 'center',
                        'transition': 'transform 0.3s ease, box-shadow 0.3s ease'
                    }),
                    
                    html.Div([
                        html.Div("🎯", style={'fontSize': '48px', 'marginBottom': '16px'}),
                        html.H3("Analizuj wyniki", style={
                            'color': LIGHT_THEME['text'],
                            'fontWeight': '700',
                            'marginBottom': '12px',
                            'fontSize': 'clamp(18px, 2vw, 24px)'
                        }),
                        html.P("Wykorzystuj zaawansowane wykresy do analizy swoich mocnych i słabych stron", style={
                            'color': LIGHT_THEME['placeholder'],
                            'fontSize': 'clamp(14px, 1.5vw, 16px)',
                            'lineHeight': '1.5'
                        })
                    ], className='card', style={
                        'background': LIGHT_THEME['content_bg'],
                        'padding': 'clamp(20px, 3vw, 32px)',
                        'borderRadius': LIGHT_THEME['radius'],
                        'boxShadow': LIGHT_THEME['shadow'],
                        'textAlign': 'center',
                        'transition': 'transform 0.3s ease, box-shadow 0.3s ease'
                    })
                ], className='card-container', style={
                    'marginTop': 'clamp(30px, 5vw, 60px)',
                    'gap': 'clamp(10px, 2vw, 20px)'
                })
            ], style={
                'background': LIGHT_THEME['content_bg'],
                'borderRadius': LIGHT_THEME['radius_large'],
                'boxShadow': LIGHT_THEME['shadow_strong'],
                'padding': 'clamp(30px, 5vw, 60px) clamp(20px, 3vw, 40px)',
                'maxWidth': '1200px',
                'margin': 'clamp(30px, 5vw, 60px) auto 0 auto',
                'backdropFilter': 'blur(10px)'
            })
        ], className='container', style={
            'padding': 'clamp(20px, 3vw, 40px)',
            'minHeight': '100vh'
        })
    ])

def get_math_tasks_layout():
    return html.Div([
        html.Div([
            html.H1("🇵🇱 Zadania Maturalne", style={
                'textAlign': 'center', 
                'color': LIGHT_THEME['text'], 
                'fontWeight': '800', 
                'marginBottom': '16px',
                'fontSize': 'clamp(28px, 4vw, 42px)'
            }),
            html.P("Organizuj swoje zadania maturalne i śledź postępy w nauce", style={
                'textAlign': 'center',
                'color': LIGHT_THEME['placeholder'],
                'fontSize': 'clamp(14px, 2vw, 18px)',
                'fontWeight': '500',
                'marginBottom': '40px'
            })
        ]),
        
        # Enhanced FAB button
        html.Button([
            html.Span("+", style={'fontSize': '28px', 'fontWeight': '800'})
        ],
            id='open-add-set-modal',
            n_clicks=0,
            title='Dodaj nowy zestaw zadań',
            style={
                'position': 'fixed',
                'bottom': '40px',
                'right': '40px',
                'width': '70px',
                'height': '70px',
                'borderRadius': '50%',
                'background': LIGHT_THEME['gradient_primary'],
                'color': '#fff',
                'fontSize': '32px',
                'fontWeight': '800',
                'boxShadow': LIGHT_THEME['shadow_strong'],
                'border': 'none',
                'zIndex': 2000,
                'cursor': 'pointer',
                'transition': 'all 0.3s ease',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center'
            },
            className='fab-button'
        ),
        
        html.Div([
            html.Div([
                html.H3("🗂️ Twoje zestawy zadań", style={
                    'marginBottom': '24px', 
                    'fontWeight': '700',
                    'color': LIGHT_THEME['text'],
                    'fontSize': 'clamp(20px, 2.5vw, 24px)'
                }),
                html.Div(id='math-tasks-list', style={'marginTop': '20px'})
            ], style={
                'background': LIGHT_THEME['content_bg'], 
                'borderRadius': LIGHT_THEME['radius_large'], 
                'boxShadow': LIGHT_THEME['shadow'], 
                'padding': 'clamp(20px, 3vw, 40px)', 
                'backdropFilter': 'blur(10px)'
            })
        ], style={'maxWidth': '1200px', 'margin': '0 auto'})
    ], style={'padding': 'clamp(20px, 3vw, 40px)'})

def get_math_tasks_list(tasks):
    import datetime
    if not tasks:
        return html.Div([
            html.Div("📝", style={'fontSize': '64px', 'textAlign': 'center', 'marginBottom': '24px'}),
            html.H3("Brak zadań", style={
                'textAlign': 'center',
                'color': LIGHT_THEME['text'],
                'fontWeight': '700',
                'marginBottom': '12px',
                'fontSize': 'clamp(20px, 2.5vw, 24px)'
            }),
            html.P("Dodaj nowy zestaw zadań, aby rozpocząć naukę!", style={
                'color': LIGHT_THEME['placeholder'], 
                'textAlign': 'center', 
                'fontSize': 'clamp(14px, 2vw, 18px)',
                'fontWeight': '500'
            })
        ], style={
            'padding': 'clamp(30px, 5vw, 60px) clamp(20px, 3vw, 40px)',
            'textAlign': 'center',
            'background': 'linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%)',
            'borderRadius': LIGHT_THEME['radius'],
            'border': f"2px dashed {LIGHT_THEME['border']}"
        })
    
    sets = {}
    for task in tasks:
        set_id = task.get('set_id', 'individual')
        if set_id not in sets:
            sets[set_id] = {
                'name': task.get('set_name', 'Pojedyncze zadania'),
                'tasks': [],
                'subject': task.get('subject', 'matematyka')
            }
        sets[set_id]['tasks'].append(task)
    
    sorted_sets = sorted(sets.items(), key=lambda x: x[1]['tasks'][0]['created'], reverse=True)
    set_sections = []
    
    for set_id, set_data in sorted_sets:
        sorted_tasks = sorted(set_data['tasks'], key=lambda x: x['number'])
        
        # Calculate set statistics
        total_tasks = len(sorted_tasks)
        solved_tasks = sum(1 for task in sorted_tasks if task['solved'])
        completion_rate = solved_tasks / total_tasks if total_tasks > 0 else 0
        
        # Subject emoji
        if set_data['subject'] == 'matematyka':
            subject_emoji = "📊"
        elif set_data['subject'] == 'informatyka':
            subject_emoji = "💻"
        elif set_data['subject'] == 'polski':
            subject_emoji = "🇵🇱"
        else:  # angielski
            subject_emoji = "🇬🇧"
        
        task_rows = []
        for task in sorted_tasks:
            tags = [html.Span([
                html.Span("🏷️", style={'marginRight': '4px', 'fontSize': '12px'}),
                tag.replace('_', ' ')
            ], style={
                'display': 'inline-block',
                'background': 'linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%)',
                'color': '#4f46e5',
                'padding': '4px 12px',
                'borderRadius': '20px',
                'margin': '0 6px 6px 0',
                'fontSize': 'clamp(11px, 1.2vw, 13px)',
                'fontWeight': '600',
                'border': '1px solid #c7d2fe'
            }) for tag in task['tags']]
            
            status_icon = "✅" if task['solved'] else "❌"
            status_color = LIGHT_THEME['status_solved'] if task['solved'] else LIGHT_THEME['status_unsolved']
            status_text = "Rozwiązane" if task['solved'] else "Nierozwiązane"
            
            content_display = html.Div(
                html.P(task['content'], style={
                    'whiteSpace': 'pre-line', 
                    'marginTop': '12px',
                    'color': LIGHT_THEME['text'],
                    'lineHeight': '1.6',
                    'fontSize': 'clamp(13px, 1.5vw, 15px)'
                }),
                style={
                    'background': 'linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%)',
                    'padding': 'clamp(12px, 2vw, 16px)',
                    'borderRadius': LIGHT_THEME['radius'],
                    'marginTop': '12px',
                    'display': 'block' if task['content'] else 'none',
                    'border': f"1px solid {LIGHT_THEME['border']}"
                }
            )
            
            task_rows.append(
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Strong(f"📝 {task['name']}", style={
                                    'fontSize': 'clamp(16px, 2vw, 18px)',
                                    'color': LIGHT_THEME['text'],
                                    'fontWeight': '700'
                                }),
                                html.Span(f" (Zadanie #{task['number']})", style={
                                    'color': LIGHT_THEME['placeholder'],
                                    'fontSize': 'clamp(12px, 1.5vw, 14px)',
                                    'fontWeight': '500',
                                    'marginLeft': '8px'
                                })
                            ], style={'marginBottom': '12px'}),
                            html.Div(tags, style={'margin': '12px 0'}),
                            content_display
                        ], style={'flex': 1}),
                        html.Div([
                            html.Div([
                                html.Span(status_icon, style={
                                    'fontSize': '20px',
                                    'marginRight': '8px'
                                }),
                                html.Span(status_text, style={
                                    'color': status_color,
                                    'fontSize': 'clamp(14px, 1.5vw, 16px)',
                                    'fontWeight': '700'
                                })
                            ], style={
                                'display': 'flex',
                                'alignItems': 'center',
                                'padding': '8px 16px',
                                'background': f"{status_color}20",
                                'borderRadius': LIGHT_THEME['radius'],
                                'border': f"2px solid {status_color}40"
                            })
                        ], style={'display': 'flex', 'alignItems': 'flex-start'})
                    ], style={
                        'display': 'flex', 
                        'alignItems': 'flex-start', 
                        'justifyContent': 'space-between',
                        'marginBottom': '16px',
                        'flexWrap': 'wrap',
                        'gap': '12px'
                    }),
                    html.Div([
                        html.Button([
                            html.Span("✏️", style={'marginRight': '6px'}),
                            "Edytuj"
                        ],
                            id={'type': 'edit-btn', 'index': task['id']},
                            n_clicks=0,
                            style={
                                'padding': 'clamp(8px, 1.5vw, 10px) clamp(16px, 2vw, 20px)',
                                'background': LIGHT_THEME['gradient_warning'],
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': LIGHT_THEME['radius'],
                                'cursor': 'pointer',
                                'marginRight': '12px',
                                'fontWeight': '600',
                                'fontSize': 'clamp(12px, 1.5vw, 14px)',
                                'boxShadow': LIGHT_THEME['shadow'],
                                'transition': 'all 0.3s ease'
                            }
                        ),
                        html.Button([
                            html.Span("🗑️", style={'marginRight': '6px'}),
                            "Usuń"
                        ],
                            id={'type': 'delete-btn', 'index': task['id']},
                            n_clicks=0,
                            style={
                                'padding': 'clamp(8px, 1.5vw, 10px) clamp(16px, 2vw, 20px)',
                                'background': LIGHT_THEME['button_danger'],
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': LIGHT_THEME['radius'],
                                'cursor': 'pointer',
                                'fontWeight': '600',
                                'fontSize': 'clamp(12px, 1.5vw, 14px)',
                                'boxShadow': LIGHT_THEME['shadow'],
                                'transition': 'all 0.3s ease'
                            }
                        )
                    ], style={
                        'display': 'flex', 
                        'justifyContent': 'flex-end',
                        'flexWrap': 'wrap',
                        'gap': '8px'
                    })
                ], style={
                    'background': 'rgba(255, 255, 255, 0.9)',
                    'padding': 'clamp(16px, 2.5vw, 24px)',
                    'margin': '16px 0',
                    'borderRadius': LIGHT_THEME['radius'],
                    'border': f"1px solid {LIGHT_THEME['border']}",
                    'boxShadow': LIGHT_THEME['shadow'],
                    'backdropFilter': 'blur(10px)',
                    'transition': 'all 0.3s ease'
                }, className='task-item')
            )
        
        # Set header with enhanced styling and responsiveness
        set_header = html.Div([
            html.Div([
                html.Div([
                    html.H4([
                        html.Span(subject_emoji, style={'marginRight': '12px', 'fontSize': '24px'}),
                        set_data['name']
                    ], style={
                        'marginBottom': '8px', 
                        'fontWeight': '800',
                        'color': 'white',
                        'fontSize': 'clamp(18px, 2.5vw, 22px)'
                    }),
                    html.Div([
                        html.Span(f"📊 {total_tasks} zadań", style={
                            'fontSize': 'clamp(12px, 1.5vw, 14px)',
                            'color': 'rgba(255,255,255,0.9)',
                            'marginRight': '16px',
                            'fontWeight': '600'
                        }),
                        html.Span(f"✅ {solved_tasks} rozwiązanych", style={
                            'fontSize': 'clamp(12px, 1.5vw, 14px)',
                            'color': 'rgba(255,255,255,0.9)',
                            'marginRight': '16px',
                            'fontWeight': '600'
                        }),
                        html.Span(f"📅 {datetime.datetime.fromisoformat(set_data['tasks'][0]['created']).strftime('%d.%m.%Y %H:%M')}", style={
                            'fontSize': 'clamp(11px, 1.3vw, 14px)',
                            'color': 'rgba(255,255,255,0.8)',
                            'fontWeight': '500'
                        })
                    ], style={'flexWrap': 'wrap', 'gap': '8px', 'display': 'flex'})
                ], style={'flex': '1'}),
                
                # Right side with dropdown menu and progress
                html.Div([
                    # Dropdown menu button
                    html.Div([
                        html.Button([
                            html.Span("⚙️", style={'fontSize': '18px'})
                        ],
                            id={'type': 'toggle-set-menu', 'index': set_id},
                            n_clicks=0,
                            style={
                                'width': '40px',
                                'height': '40px',
                                'borderRadius': '50%',
                                'background': 'rgba(255,255,255,0.2)',
                                'color': 'white',
                                'border': '1px solid rgba(255,255,255,0.3)',
                                'cursor': 'pointer',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'transition': 'all 0.3s ease',
                                'marginRight': '16px'
                            }
                        )
                    ], style={
                        'position': 'relative',
                        'zIndex': '1'
                    }),
                    
                    # Progress section (always visible)
                    html.Div([
                        html.Div([
                            html.Span(f"{completion_rate*100:.0f}%", style={
                                'fontSize': 'clamp(20px, 2.5vw, 24px)',
                                'fontWeight': '800',
                                'color': LIGHT_THEME['success'] if completion_rate > 0.7 else LIGHT_THEME['warning'] if completion_rate > 0.3 else LIGHT_THEME['error'],
                                'marginBottom': '4px',
                                'display': 'block'
                            }),
                            html.Div(style={
                                'width': 'clamp(60px, 8vw, 80px)',
                                'height': '8px',
                                'background': 'rgba(255,255,255,0.3)',
                                'borderRadius': '4px',
                                'overflow': 'hidden'
                            }, children=[
                                html.Div(style={
                                    'width': f"{completion_rate*100}%",
                                    'height': '100%',
                                    'background': LIGHT_THEME['success'] if completion_rate > 0.7 else LIGHT_THEME['warning'] if completion_rate > 0.3 else LIGHT_THEME['error'],
                                    'transition': 'width 0.5s ease',
                                    'borderRadius': '4px'
                                })
                            ])
                        ], style={'textAlign': 'center'})
                    ])
                ], style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '8px'})
            ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'flexWrap': 'wrap', 'gap': '16px'})
        ], style={
            'margin': '32px 0 20px 0',
            'padding': 'clamp(16px, 2.5vw, 24px)',
            'background': LIGHT_THEME['gradient_primary'],
            'color': 'white',
            'borderRadius': LIGHT_THEME['radius'],
            'boxShadow': LIGHT_THEME['shadow_strong'],
            'backdropFilter': 'blur(10px)'
        })
        
        dropdown_menu = html.Div([
            html.Button([
                html.Span("➕", style={'marginRight': '8px'}),
                "Dodaj zadanie"
            ],
                id={'type': 'add-task-to-set-btn', 'index': set_id},
                n_clicks=0,
                style={
                    'width': '100%',
                    'padding': '12px 16px',
                    'background': 'rgba(102, 126, 234, 0.9)',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '8px',
                    'cursor': 'pointer',
                    'fontWeight': '600',
                    'fontSize': 'clamp(12px, 1.5vw, 14px)',
                    'marginBottom': '8px',
                    'transition': 'all 0.3s ease',
                    'textAlign': 'left'
                }
            ),
            html.Button([
                html.Span("✏️", style={'marginRight': '8px'}),
                "Edytuj zestaw"
            ],
                id={'type': 'edit-set-btn', 'index': set_id},
                n_clicks=0,
                style={
                    'width': '100%',
                    'padding': '12px 16px',
                    'background': 'rgba(243, 156, 18, 0.9)',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '8px',
                    'cursor': 'pointer',
                    'fontWeight': '600',
                    'fontSize': 'clamp(12px, 1.5vw, 14px)',
                    'marginBottom': '8px',
                    'transition': 'all 0.3s ease',
                    'textAlign': 'left'
                }
            ),
            html.Button([
                html.Span("🗑️", style={'marginRight': '8px'}),
                "Usuń zestaw"
            ],
                id={'type': 'delete-set-btn', 'index': set_id},
                n_clicks=0,
                style={
                    'width': '100%',
                    'padding': '12px 16px',
                    'background': 'rgba(220, 53, 69, 0.9)',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '8px',
                    'cursor': 'pointer',
                    'fontWeight': '600',
                    'fontSize': 'clamp(12px, 1.5vw, 14px)',
                    'transition': 'all 0.3s ease',
                    'textAlign': 'left'
                }
            )
        ], 
            id={'type': 'set-dropdown-menu', 'index': set_id},
            style={
                'position': 'absolute',
                'top': '50px',
                'right': 'clamp(80px, 10vw, 100px)',
                'background': 'white',
                'borderRadius': '12px',
                'boxShadow': '0 8px 32px rgba(0,0,0,0.25)',
                'padding': '16px',
                'minWidth': 'clamp(180px, 20vw, 200px)',
                'zIndex': '9999',
                'border': '1px solid rgba(0,0,0,0.1)',
                'display': 'none'
            }
        )
        
        set_sections.append(html.Div([
            set_header,
            dropdown_menu,
            html.Div(task_rows)
        ], style={
            'marginBottom': '40px',
            'position': 'relative'
        }))
    
    return html.Div(set_sections)

def get_stats_layout(subject="matematyka"):
    from utils import fetch_all_zestawy, fetch_zadania_for_zestaw
    zestawy = fetch_all_zestawy()
    zestawy_filtered = [z for z in zestawy if z.get('subject', 'matematyka') == subject]
    
    # Subject specific styling
    if subject == "matematyka":
        subject_emoji = "📊"
        subject_color = LIGHT_THEME['gradient_primary']
    elif subject == "informatyka":
        subject_emoji = "💻"
        subject_color = LIGHT_THEME['gradient_secondary']
    elif subject == "polski":
        subject_emoji = "🇵🇱"
        subject_color = LIGHT_THEME['gradient_primary']  # Use primary color for Polish
    else:  # angielski
        subject_emoji = "🇬🇧"
        subject_color = LIGHT_THEME['gradient_secondary']  # Use secondary color for English

    zestawy_div = html.Div([
        html.Div([
            html.H3([
                html.Span("🗂️", style={'marginRight': '12px', 'fontSize': '28px'}),
                "Twoje zestawy zadań"
            ], style={
                'marginBottom': '24px', 
                'fontWeight': '800',
                'color': LIGHT_THEME['text'],
                'fontSize': 'clamp(22px, 3vw, 26px)'
            }),
            html.Div([
                html.Div([
                    html.Div([
                        html.H4([
                            html.Span(subject_emoji, style={'marginRight': '8px'}),
                            f"{z['name']}"
                        ], style={
                            'marginBottom': '12px',
                            'fontWeight': '700',
                            'color': LIGHT_THEME['text'],
                            'fontSize': 'clamp(18px, 2.5vw, 20px)'
                        }),
                        html.Div([
                            html.Span("📅", style={'marginRight': '6px'}),
                            f"{z['created_at'].strftime('%d.%m.%Y %H:%M') if hasattr(z['created_at'], 'strftime') else z['created_at']}"
                        ], style={
                            'fontSize': 'clamp(12px, 1.5vw, 14px)',
                            'color': LIGHT_THEME['placeholder'],
                            'marginBottom': '16px',
                            'fontWeight': '500'
                        }),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Strong(f"📝 {zad['nr_zadania']}. {zad['nazwa']}", style={
                                        'color': LIGHT_THEME['text'],
                                        'fontSize': 'clamp(14px, 1.8vw, 16px)'
                                    }),
                                    html.Div([
                                        html.Span("✅ Rozwiązane" if zad['solved'] else "❌ Nierozwiązane", style={
                                            'color': LIGHT_THEME['success'] if zad['solved'] else LIGHT_THEME['error'],
                                            'fontWeight': '600',
                                            'fontSize': 'clamp(12px, 1.5vw, 14px)',
                                            'marginLeft': '12px'
                                        })
                                    ]),
                                    html.Div([
                                        html.Span("🏷️ Tagi: ", style={
                                            'fontSize': 'clamp(11px, 1.3vw, 13px)',
                                            'color': LIGHT_THEME['text'],
                                            'fontWeight': '600'
                                        }),
                                        html.Span(', '.join(zad['tags']) if zad['tags'] else 'Brak tagów', style={
                                            'fontSize': 'clamp(11px, 1.3vw, 13px)',
                                            'color': LIGHT_THEME['placeholder']
                                        })
                                    ], style={'marginTop': '4px'}),
                                    html.Div([
                                        html.P(zad['tresc'] if zad['tresc'] else 'Brak treści', style={
                                            'fontSize': 'clamp(11px, 1.3vw, 13px)',
                                            'color': LIGHT_THEME['placeholder'],
                                            'fontStyle': 'italic' if not zad['tresc'] else 'normal',
                                            'margin': '8px 0 0 0',
                                            'lineHeight': '1.4'
                                        })
                                    ])
                                ], style={
                                    'padding': 'clamp(12px, 2vw, 16px)',
                                    'background': 'rgba(255, 255, 255, 0.7)',
                                    'borderRadius': LIGHT_THEME['radius'],
                                    'marginBottom': '12px',
                                    'border': f"1px solid {LIGHT_THEME['border']}",
                                    'transition': 'all 0.3s ease'
                                })
                                for zad in fetch_zadania_for_zestaw(z['id'])
                            ])
                        ]) if fetch_zadania_for_zestaw(z['id']) else html.Div([
                            html.Div("📝", style={'fontSize': '48px', 'textAlign': 'center', 'marginBottom': '16px'}),
                            html.P("Brak zadań w zestawie", style={
                                'color': LIGHT_THEME['placeholder'],
                                'fontSize': 'clamp(14px, 1.8vw, 16px)',
                                'textAlign': 'center',
                                'fontStyle': 'italic'
                            })
                        ], style={
                            'padding': 'clamp(30px, 4vw, 40px)',
                            'background': 'rgba(255, 255, 255, 0.5)',
                            'borderRadius': LIGHT_THEME['radius'],
                            'border': f"2px dashed {LIGHT_THEME['border']}"
                        })
                    ], style={
                        'background': 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%)',
                        'padding': 'clamp(16px, 2.5vw, 24px)',
                        'borderRadius': LIGHT_THEME['radius'],
                        'boxShadow': LIGHT_THEME['shadow'],
                        'marginBottom': '24px',
                        'backdropFilter': 'blur(10px)',
                        'border': f"1px solid {LIGHT_THEME['border']}"
                    })
                    for z in zestawy_filtered
                ])
            ]) if zestawy_filtered else html.Div([
                html.Div("📂", style={'fontSize': '64px', 'textAlign': 'center', 'marginBottom': '24px'}),
                html.H3("Brak zestawów", style={
                    'textAlign': 'center',
                    'color': LIGHT_THEME['text'],
                    'fontWeight': '700',
                    'marginBottom': '12px',
                    'fontSize': 'clamp(20px, 2.5vw, 24px)'
                }),
                html.P(f"Nie masz jeszcze żadnych zestawów dla przedmiotu {subject}.", style={
                    'color': LIGHT_THEME['placeholder'],
                    'textAlign': 'center',
                    'fontSize': 'clamp(16px, 2vw, 18px)',
                    'fontWeight': '500'
                })
            ], style={
                'padding': 'clamp(40px, 5vw, 60px) clamp(30px, 4vw, 40px)',
                'textAlign': 'center',
                'background': 'linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%)',
                'borderRadius': LIGHT_THEME['radius'],
                'border': f"2px dashed {LIGHT_THEME['border']}"
            })
        ])
    ], style={
        'marginTop': '40px',
        'background': LIGHT_THEME['content_bg'],
        'padding': 'clamp(20px, 3vw, 32px)',
        'borderRadius': LIGHT_THEME['radius_large'],
        'boxShadow': LIGHT_THEME['shadow'],
        'backdropFilter': 'blur(10px)'
    })

    return html.Div([
        html.Div([
            html.H1([
                html.Span(subject_emoji, style={'marginRight': '16px'}),
                f"Statystyki Zadań ({subject.capitalize()})"
            ], style={
                'textAlign': 'center',
                'color': LIGHT_THEME['text'],
                'fontWeight': '800',
                'marginBottom': '16px',
                'fontSize': 'clamp(28px, 4vw, 42px)',
                'background': subject_color,
                'WebkitBackgroundClip': 'text',
                'WebkitTextFillColor': 'transparent',
                'backgroundClip': 'text'
            }),
            html.P(f"Analizuj swoje wyniki i postępy w nauce {subject}", style={
                'textAlign': 'center',
                'color': LIGHT_THEME['placeholder'],
                'fontSize': 'clamp(16px, 2vw, 18px)',
                'fontWeight': '500',
                'marginBottom': '40px'
            })
        ]),
        
        html.Div([
            html.Div([
                dcc.Graph(
                    id=f'stats-graph-{"it" if subject=="informatyka" else "polski" if subject=="polski" else "angielski" if subject=="angielski" else "math"}',
                    style={
                        'background': 'transparent',
                        'borderRadius': LIGHT_THEME['radius']
                    }
                ),
                html.Div(
                    id=f'stats-summary-{"it" if subject=="informatyka" else "polski" if subject=="polski" else "angielski" if subject=="angielski" else "math"}',
                    style={'marginTop': '32px'}
                )
            ], style={
                'background': LIGHT_THEME['content_bg'],
                'borderRadius': LIGHT_THEME['radius_large'],
                'boxShadow': LIGHT_THEME['shadow_strong'],
                'padding': 'clamp(20px, 3vw, 40px)',
                'backdropFilter': 'blur(10px)'
            })
        ], style={'maxWidth': '1200px', 'margin': '0 auto', 'marginBottom': '40px'}),
        
        zestawy_div
    ], style={'padding': 'clamp(20px, 3vw, 40px)'})

def get_stats_layout_it():
    return get_stats_layout(subject="informatyka")

def get_stats_layout_polski():
    return get_stats_layout(subject="polski")

def get_stats_layout_angielski():
    return get_stats_layout(subject="angielski")

def get_manage_categories_layout():
    return html.Div([
        html.Div([
            html.Div([
                html.H1([
                    html.Span("🏷️", style={'marginRight': '16px'}),
                    "Zarządzaj Kategoriami"
                ], style={
                    'color': LIGHT_THEME['text'],
                    'fontWeight': '800',
                    'fontSize': '36px',
                    'marginBottom': '8px',
                    'textAlign': 'center'
                }),
                html.P("Dodawaj i zarządzaj kategoriami dla swoich zestawów zadań", style={
                    'color': LIGHT_THEME['placeholder'],
                    'fontSize': '18px',
                    'textAlign': 'center',
                    'marginBottom': '40px',
                    'fontWeight': '500'
                })
            ], style={
                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'padding': '60px 40px',
                'borderRadius': f"{LIGHT_THEME['radius']} {LIGHT_THEME['radius']} 0 0",
                'color': 'white',
                'textAlign': 'center'
            }),
            
            html.Div([
                # Sekcja dodawania kategorii
                html.Div([
                    html.H2([
                        html.Span("➕", style={'marginRight': '12px'}),
                        "Dodaj Nową Kategorię"
                    ], style={
                        'color': LIGHT_THEME['text'],
                        'fontWeight': '700',
                        'fontSize': '24px',
                        'marginBottom': '24px'
                    }),
                    
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
                                id='category-subject-dropdown',
                                options=[
                                    {'label': '∑ Matematyka', 'value': 'matematyka'},
                                    {'label': '💻 Informatyka', 'value': 'informatyka'},
                                    {'label': '🇵🇱 Język Polski', 'value': 'polski'},
                                    {'label': '🇬🇧 Język Angielski', 'value': 'angielski'}
                                ],
                                placeholder="Wybierz przedmiot...",
                                style={
                                    'marginBottom': '20px',
                                    'borderRadius': LIGHT_THEME['radius']
                                }
                            )
                        ], style={'flex': '1', 'marginRight': '20px'}),
                        
                        html.Div([
                            html.Label("🏷️ Nazwa kategorii:", style={
                                'display': 'block',
                                'marginBottom': '8px',
                                'fontWeight': '700',
                                'color': LIGHT_THEME['text'],
                                'fontSize': '16px'
                            }),
                            dcc.Input(
                                id='new-category-name',
                                type='text',
                                placeholder='Np. "Geometria Analityczna"',
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
                            )
                        ], style={'flex': '1'})
                    ], style={'display': 'flex', 'marginBottom': '24px'}),
                    
                    html.Div([
                        html.Button([
                            html.Span("💾", style={'marginRight': '8px'}),
                            'Dodaj Kategorię'
                        ],
                        id='add-category-button',
                        n_clicks=0,
                        style={
                            'padding': '16px 32px',
                            'background': LIGHT_THEME['success'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': LIGHT_THEME['radius'],
                            'cursor': 'pointer',
                            'fontWeight': '700',
                            'fontSize': '16px',
                            'boxShadow': LIGHT_THEME['shadow']
                        })
                    ], style={'textAlign': 'center', 'marginBottom': '32px'}),
                    
                    html.Div(id='category-message', style={
                        'textAlign': 'center',
                        'marginBottom': '32px',
                        'fontSize': '16px',
                        'fontWeight': '600'
                    })
                ], style={
                    'background': LIGHT_THEME['content_bg'],
                    'padding': '32px',
                    'borderRadius': LIGHT_THEME['radius'],
                    'boxShadow': LIGHT_THEME['shadow'],
                    'marginBottom': '32px'
                }),
                
                # Sekcja listy kategorii
                html.Div([
                    html.H2([
                        html.Span("📋", style={'marginRight': '12px'}),
                        "Istniejące Kategorie"
                    ], style={
                        'color': LIGHT_THEME['text'],
                        'fontWeight': '700',
                        'fontSize': '24px',
                        'marginBottom': '24px'
                    }),
                    
                    html.Div([
                        html.Label("🔍 Filtruj według przedmiotu:", style={
                            'display': 'block',
                            'marginBottom': '8px',
                            'fontWeight': '700',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '16px'
                        }),
                        dcc.Dropdown(
                            id='filter-subject-dropdown',
                            options=[
                                {'label': 'Wszystkie przedmioty', 'value': 'all'},
                                {'label': '∑ Matematyka', 'value': 'matematyka'},
                                {'label': '💻 Informatyka', 'value': 'informatyka'},
                                {'label': '🇵🇱 Język Polski', 'value': 'polski'},
                                {'label': '🇬🇧 Język Angielski', 'value': 'angielski'}
                            ],
                            value='all',
                            style={
                                'marginBottom': '24px',
                                'borderRadius': LIGHT_THEME['radius']
                            }
                        )
                    ]),
                    
                    html.Div(id='categories-list', style={
                        'minHeight': '200px'
                    })
                ], style={
                    'background': LIGHT_THEME['content_bg'],
                    'padding': '32px',
                    'borderRadius': LIGHT_THEME['radius'],
                    'boxShadow': LIGHT_THEME['shadow']
                })
            ], style={'padding': '40px'})
        ], style={
            'background': LIGHT_THEME['content_bg'],
            'minHeight': '100vh',
            'borderRadius': LIGHT_THEME['radius'],
            'boxShadow': LIGHT_THEME['shadow'],
            'overflow': 'hidden'
        })
    ], style={
        'padding': '20px',
        'background': LIGHT_THEME['background'],
        'minHeight': '100vh'
    })

def get_settings_layout(theme_name='light'):
    theme = get_theme(theme_name)
    return html.Div([
        html.Div([
            html.H1([
                html.Span("⚙️", style={'marginRight': '16px'}),
                "Ustawienia"
            ], style={
                'textAlign': 'center',
                'color': theme['text'],
                'fontWeight': '800',
                'marginBottom': '16px',
                'fontSize': 'clamp(28px, 4vw, 42px)'
            }),
            html.P("Zarządzaj ustawieniami aplikacji", style={
                'textAlign': 'center',
                'color': theme['placeholder'],
                'fontSize': 'clamp(16px, 2vw, 18px)',
                'fontWeight': '500',
                'marginBottom': '40px'
            })
        ]),
        
        html.Div([
            # Theme Settings Section
            html.Div([
                html.H2([
                    html.Span("🎨", style={'marginRight': '12px'}),
                    "Motyw"
                ], style={
                    'color': theme['text'],
                    'fontWeight': '700',
                    'fontSize': '24px',
                    'marginBottom': '24px'
                }),
                
                html.Div([
                    html.Label("Wybierz motyw aplikacji:", style={
                        'display': 'block',
                        'marginBottom': '12px',
                        'fontWeight': '600',
                        'color': theme['text'],
                        'fontSize': '16px'
                    }),
                    
                    html.Div([
                        html.Div([
                            dcc.RadioItems(
                                id='theme-selector',
                                options=[
                                    {
                                        'label': html.Div([
                                            html.Span("☀️", style={'marginRight': '8px', 'fontSize': '20px'}),
                                            "Jasny"
                                        ], style={'display': 'flex', 'alignItems': 'center'}),
                                        'value': 'light'
                                    },
                                    {
                                        'label': html.Div([
                                            html.Span("🌙", style={'marginRight': '8px', 'fontSize': '20px'}),
                                            "Ciemny"
                                        ], style={'display': 'flex', 'alignItems': 'center'}),
                                        'value': 'dark'
                                    }
                                ],
                                value=theme_name,
                                style={
                                    'fontSize': '16px',
                                    'fontWeight': '600'
                                },
                                inputStyle={'marginRight': '8px'}
                            )
                        ])
                    ], style={
                        'background': theme['content_bg'],
                        'padding': '20px',
                        'borderRadius': theme['radius'],
                        'border': f"1px solid {theme['border']}",
                        'marginBottom': '32px'
                    })
                ])
            ], style={
                'background': theme['content_bg'],
                'padding': 'clamp(20px, 3vw, 32px)',
                'borderRadius': theme['radius_large'],
                'boxShadow': theme['shadow'],
                'marginBottom': '32px',
                'backdropFilter': 'blur(10px)'
            }),
            
            # Database Management Section
            html.Div([
                html.H2([
                    html.Span("🗄️", style={'marginRight': '12px'}),
                    "Zarządzanie Bazą Danych"
                ], style={
                    'color': theme['text'],
                    'fontWeight': '700',
                    'fontSize': '24px',
                    'marginBottom': '16px'
                }),
                
                html.P("⚠️ Uwaga: Te operacje są nieodwracalne!", style={
                    'color': theme['error'],
                    'fontSize': '16px',
                    'fontWeight': '600',
                    'marginBottom': '24px',
                    'textAlign': 'center'
                }),
                
                html.Div([
                    html.Button([
                        html.Span("🏷️", style={'marginRight': '8px'}),
                        'Wyczyść Wszystkie Kategorie'
                    ],
                    id='settings-clear-categories-button',
                    n_clicks=0,
                    style={
                        'width': '100%',
                        'padding': '16px',
                        'background': theme['warning'],
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': theme['radius'],
                        'cursor': 'pointer',
                        'fontWeight': '700',
                        'fontSize': '16px',
                        'boxShadow': theme['shadow'],
                        'marginBottom': '12px',
                        'transition': 'all 0.3s ease'
                    }),
                    
                    html.Button([
                        html.Span("📝", style={'marginRight': '8px'}),
                        'Wyczyść Wszystkie Zadania'
                    ],
                    id='settings-clear-tasks-button',
                    n_clicks=0,
                    style={
                        'width': '100%',
                        'padding': '16px',
                        'background': theme['error'],
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': theme['radius'],
                        'cursor': 'pointer',
                        'fontWeight': '700',
                        'fontSize': '16px',
                        'boxShadow': theme['shadow'],
                        'marginBottom': '12px',
                        'transition': 'all 0.3s ease'
                    }),
                    
                    html.Button([
                        html.Span("💣", style={'marginRight': '8px'}),
                        'Wyczyść Całą Bazę Danych'
                    ],
                    id='settings-clear-all-button',
                    n_clicks=0,
                    style={
                        'width': '100%',
                        'padding': '16px',
                        'background': '#8b0000',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': theme['radius'],
                        'cursor': 'pointer',
                        'fontWeight': '700',
                        'fontSize': '16px',
                        'boxShadow': theme['shadow'],
                        'marginBottom': '24px',
                        'transition': 'all 0.3s ease'
                    })
                ])
            ], style={
                'background': theme['content_bg'],
                'padding': 'clamp(20px, 3vw, 32px)',
                'borderRadius': theme['radius_large'],
                'boxShadow': theme['shadow'],
                'backdropFilter': 'blur(10px)'
            }),
            
            # Settings message area
            html.Div(id='settings-message', style={
                'textAlign': 'center',
                'marginTop': '24px',
                'fontSize': '16px',
                'fontWeight': '600'
            })
            
        ], style={'maxWidth': '800px', 'margin': '0 auto'})
    ], style={'padding': 'clamp(20px, 3vw, 40px)'})

