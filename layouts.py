# layouts.py
from dash import dcc, html
from theme import LIGHT_THEME
from utils import TAGS

def get_sidebar():
    return html.Div([
        html.H2("LifeChanger", style={'color': LIGHT_THEME['text_light'], 'padding': '24px 0 16px 0', 'fontWeight': 'bold', 'letterSpacing': '2px', 'textAlign': 'center'}),
        html.Ul([
            html.Li(
                dcc.Link("Strona Główna", href="/", style={'color': LIGHT_THEME['text_light'], 'fontWeight': 'bold', 'fontSize': '18px', 'textDecoration': 'none', 'transition': 'color 0.2s'}),
                style={'padding': '16px 32px', 'borderBottom': '1px solid #34495e', 'transition': 'background 0.2s'}
            ),
            html.Li(
                dcc.Link("Zadania Maturalne", href="/math-tasks", style={'color': LIGHT_THEME['text_light'], 'fontWeight': 'bold', 'fontSize': '18px', 'textDecoration': 'none', 'transition': 'color 0.2s'}),
                style={'padding': '16px 32px', 'borderBottom': '1px solid #34495e', 'transition': 'background 0.2s'}
            ),
            html.Li(
                dcc.Link("Statystyki", href="/stats", style={'color': LIGHT_THEME['text_light'], 'fontWeight': 'bold', 'fontSize': '18px', 'textDecoration': 'none', 'transition': 'color 0.2s'}),
                style={'padding': '16px 32px', 'transition': 'background 0.2s'}
            ),
        ], style={'listStyleType': 'none', 'padding': 0, 'margin': 0}),
    ], style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '260px',
        'background': LIGHT_THEME['sidebar_bg'],
        'boxShadow': LIGHT_THEME['shadow'],
        'zIndex': 100,
        'borderTopRightRadius': LIGHT_THEME['radius'],
        'borderBottomRightRadius': LIGHT_THEME['radius']
    })

def get_home_layout():
    return html.Div([
        html.H1("Witaj w LifeChanger!", style={'textAlign': 'center', 'color': LIGHT_THEME['text'], 'fontWeight': 'bold', 'marginTop': '40px'}),
        html.P("Zarządzaj zadaniami maturalnymi, śledź postępy i analizuj statystyki.", style={'textAlign': 'center', 'fontSize': '20px', 'color': LIGHT_THEME['text'], 'marginTop': '18px'})
    ])

def get_math_tasks_layout():
    return html.Div([
        html.H1("Zadania Maturalne", style={'textAlign': 'center', 'color': LIGHT_THEME['text'], 'fontWeight': 'bold', 'marginBottom': '24px'}),
        # FAB button
        html.Button(
            '+',
            id='open-add-set-modal',
            n_clicks=0,
            title='Dodaj nowy zestaw',
            style={
                'position': 'fixed',
                'bottom': '40px',
                'right': '60px',
                'width': '64px',
                'height': '64px',
                'borderRadius': '50%',
                'background': LIGHT_THEME['button_primary'],
                'color': '#fff',
                'fontSize': '38px',
                'fontWeight': 'bold',
                'boxShadow': LIGHT_THEME['shadow'],
                'border': 'none',
                'zIndex': 2000,
                'cursor': 'pointer',
                'transition': 'background 0.2s',
            }
        ),
        html.Div([
            html.H3("Twoje zestawy zadań", style={'marginTop': '20px', 'fontWeight': 'bold'}),
            html.Div(id='math-tasks-list', style={'marginTop': '20px'})
        ], style={'background': LIGHT_THEME['content_bg'], 'borderRadius': LIGHT_THEME['radius'], 'boxShadow': LIGHT_THEME['shadow'], 'padding': '32px', 'maxWidth': '900px', 'margin': '0 auto'})
    ], style={'padding': '32px'})

def get_math_tasks_list(tasks):
    import datetime
    if not tasks:
        return html.P("Brak zadań - dodaj nowy zestaw zadań!", style={'color': '#95a5a6', 'textAlign': 'center', 'padding': '20px'})
    sets = {}
    for task in tasks:
        set_id = task.get('set_id', 'individual')
        if set_id not in sets:
            sets[set_id] = {
                'name': task.get('set_name', 'Pojedyncze zadania'),
                'tasks': []
            }
        sets[set_id]['tasks'].append(task)
    sorted_sets = sorted(sets.items(), key=lambda x: x[1]['tasks'][0]['created'], reverse=True)
    set_sections = []
    for set_id, set_data in sorted_sets:
        sorted_tasks = sorted(set_data['tasks'], key=lambda x: x['number'])
        task_rows = []
        for task in sorted_tasks:
            tags = [html.Span(tag, style={
                'display': 'inline-block',
                'background': '#e0e7ff',
                'color': '#4f46e5',
                'padding': '2px 8px',
                'borderRadius': '4px',
                'margin': '0 5px 5px 0',
                'fontSize': '14px'
            }) for tag in task['tags']]
            status_icon = "✅" if task['solved'] else "❌"
            status_color = LIGHT_THEME['success'] if task['solved'] else LIGHT_THEME['error']
            status_text = "Rozwiązane" if task['solved'] else "Nierozwiązane"
            content_display = html.Div(
                html.P(task['content'], style={'whiteSpace': 'pre-line', 'marginTop': '10px'}),
                style={
                    'background': '#f8f9fa',
                    'padding': '10px',
                    'borderRadius': '4px',
                    'marginTop': '10px',
                    'display': 'block' if task['content'] else 'none'
                }
            )
            task_rows.append(
                html.Div([
                    html.Div([
                        html.Div([
                            html.Strong(f"{task['name']} (Zadanie #{task['number']})"),
                            html.Div(tags, style={'margin': '10px 0'}),
                            content_display
                        ], style={'flex': 1}),
                        html.Div([
                            html.Span(f"Status: ", style={'marginRight': '5px'}),
                            html.Span(
                                f"{status_icon} {status_text}",
                                style={
                                    'color': status_color,
                                    'fontSize': '16px',
                                    'fontWeight': 'bold'
                                }
                            )
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    ], style={'display': 'flex', 'alignItems': 'flex-start', 'justifyContent': 'space-between'}),
                    html.Div([
                        html.Button(
                            "Edytuj",
                            id={'type': 'edit-btn', 'index': task['id']},
                            n_clicks=0,
                            style={
                                'padding': '7px 16px',
                                'background': LIGHT_THEME['warning'],
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': LIGHT_THEME['radius'],
                                'cursor': 'pointer',
                                'marginRight': '8px',
                                'fontWeight': 'bold',
                                'boxShadow': LIGHT_THEME['shadow']
                            }
                        ),
                        html.Button(
                            "Usuń",
                            id={'type': 'delete-btn', 'index': task['id']},
                            n_clicks=0,
                            style={
                                'padding': '7px 16px',
                                'background': LIGHT_THEME['button_danger'],
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': LIGHT_THEME['radius'],
                                'cursor': 'pointer',
                                'fontWeight': 'bold',
                                'boxShadow': LIGHT_THEME['shadow']
                            }
                        )
                    ], style={'marginTop': '10px', 'display': 'flex', 'justifyContent': 'flex-end'})
                ], style={
                    'background': '#ffffff',
                    'padding': '20px',
                    'margin': '10px 0',
                    'borderRadius': LIGHT_THEME['radius'],
                    'border': f"1.5px solid {LIGHT_THEME['border']}",
                    'boxShadow': LIGHT_THEME['shadow']
                })
            )
        set_header = html.Div([
            html.H4(set_data['name'], style={'marginBottom': '5px', 'fontWeight': 'bold'}),
            html.Span(
                f"{len(set_data['tasks'])} zadań • {datetime.datetime.fromisoformat(set_data['tasks'][0]['created']).strftime('%Y-%m-%d %H:%M')}",
                style={'fontSize': '14px', 'color': '#7f8c8d'}
            )
        ], style={
            'margin': '20px 0 10px 0',
            'padding': '10px',
            'background': LIGHT_THEME['sidebar_bg'],
            'color': 'white',
            'borderRadius': LIGHT_THEME['radius']
        })
        set_sections.append(html.Div([set_header] + task_rows))
    return html.Div(set_sections)

def get_stats_layout():
    return html.Div([
        html.H1("Statystyki Zadań", style={'textAlign': 'center', 'color': LIGHT_THEME['text'], 'fontWeight': 'bold', 'marginBottom': '24px'}),
        html.Div([
            dcc.Graph(id='stats-graph', style={'background': 'transparent', 'borderRadius': LIGHT_THEME['radius']}),
            html.Div(id='stats-summary', style={'marginTop': '30px', 'fontSize': '18px'})
        ], style={'background': LIGHT_THEME['content_bg'], 'borderRadius': LIGHT_THEME['radius'], 'boxShadow': LIGHT_THEME['shadow'], 'padding': '32px', 'maxWidth': '900px', 'margin': '0 auto'})
    ], style={'padding': '32px'})
