# callbacks.py
from dash import dcc, html, Input, Output, State, ALL
from dash import callback, no_update
import uuid
import datetime
from utils import TAGS, get_tags_for_subject, calculate_tag_stats, create_radar_chart, create_stats_summary
from theme import LIGHT_THEME

# --- CALLBACKS ---
def register_callbacks(app):
    from dash import callback_context
    from utils import fetch_all_zestawy, fetch_zadania_for_zestaw, fetch_all_zadania_with_tags

    @app.callback(
        Output('page-content', 'children', allow_duplicate=True),
        Input('url', 'pathname'),
        prevent_initial_call=True
    )
    def display_page(pathname):
        from layouts import get_home_layout, get_stats_layout, get_stats_layout_it, get_math_tasks_layout
        if pathname == '/':
            return get_home_layout()
        elif pathname == '/math-tasks':
            return get_math_tasks_layout()
        elif pathname == '/stats':
            return get_stats_layout(subject="matematyka")
        elif pathname == '/stats-it':
            return get_stats_layout_it()
        else:
            return html.Div("404: Nie znaleziono strony", style={'padding': '40px', 'fontSize': '24px'})

    # Right side panel visibility
    @app.callback(
        [Output('add-set-modal', 'style'),
         Output('panel-overlay', 'style')],
        [Input('open-add-set-modal', 'n_clicks'),
         Input('close-add-set-modal', 'n_clicks'),
         Input('save-task-set-button', 'n_clicks'),
         Input('panel-overlay', 'n_clicks')],
        prevent_initial_call=False
    )
    def toggle_side_panel(open_clicks, close_clicks, save_clicks, overlay_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return {'display': 'none'}, {'display': 'none'}
        
        trigger = ctx.triggered[0]['prop_id']
        
        if 'open-add-set-modal' in trigger and open_clicks:
            return {'display': 'block'}, {'display': 'block'}
        elif any(['close-add-set-modal' in trigger, 'save-task-set-button' in trigger, 'panel-overlay' in trigger]):
            return {'display': 'none'}, {'display': 'none'}
        
        return {'display': 'none'}, {'display': 'none'}

    # Edit modal visibility (keeping center modal)
    @app.callback(
        Output('edit-modal', 'style'),
        [Input({'type': 'edit-btn', 'index': ALL}, 'n_clicks'),
         Input('cancel-edit-button', 'n_clicks'),
         Input('save-edit-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def toggle_edit_modal(edit_clicks, cancel_clicks, save_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return {'display': 'none'}
        trigger = ctx.triggered[0]['prop_id']
        if 'cancel-edit-button' in trigger or 'save-edit-button' in trigger:
            return {'display': 'none'}
        if 'edit-btn' in trigger and any(edit_clicks):
            return {'display': 'block'}
        return {'display': 'none'}

    @app.callback(
        Output('task-set-form-container', 'children'),
        Output('save-task-set-button', 'disabled'),
        Output('task-set-store', 'data'),
        Input('generate-task-form-button', 'n_clicks'),
        State('task-set-size', 'value'),
        State('task-set-name', 'value'),
        State('subject-dropdown', 'value'),
        State('task-set-store', 'data')
    )
    def generate_task_form(n_clicks, task_count, set_name, subject, task_set_data):
        if n_clicks == 0 or task_count is None or task_count < 1:
            return no_update, no_update, no_update
        
        set_id = str(uuid.uuid4())
        tasks = []
        for i in range(1, task_count + 1):
            task_id = str(uuid.uuid4())
            tasks.append({
                'id': task_id,
                'number': i,
                'name': '',
                'content': '',
                'tags': [],
                'solved': False,
                'temp_data': None
            })
        
        tag_options = [{'label': tag.replace('_', ' '), 'value': tag} for tag in get_tags_for_subject(subject)]
        form_children = []
        
        for task in tasks:
            form_children.append(
                html.Div([
                    html.Div([
                        html.H4(f"📝 Zadanie {task['number']}", style={
                            'marginBottom': '16px',
                            'fontWeight': '800',
                            'color': 'white',
                            'fontSize': '18px',
                            'padding': '12px 16px',
                            'background': f"linear-gradient(90deg, {LIGHT_THEME['gradient_primary']}, transparent)",
                            'borderRadius': LIGHT_THEME['radius']
                        }),
                        
                        html.Label("📝 Nazwa:", style={
                            'display': 'block',
                            'marginBottom': '6px',
                            'fontWeight': '600',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '14px'
                        }),
                        dcc.Input(
                            id={'type': 'task-name-input', 'index': task['id']},
                            type='text',
                            placeholder=f'Zadanie {task["number"]}',
                            style={
                                'width': '100%',
                                'padding': '10px',
                                'border': f"1px solid {LIGHT_THEME['border']}",
                                'borderRadius': LIGHT_THEME['radius'],
                                'fontSize': '14px',
                                'marginBottom': '12px',
                                'background': LIGHT_THEME['input_bg']
                            }
                        ),
                        
                        html.Label("📄 Treść:", style={
                            'display': 'block',
                            'marginBottom': '6px',
                            'fontWeight': '600',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '14px'
                        }),
                        dcc.Textarea(
                            id={'type': 'task-content-textarea', 'index': task['id']},
                            placeholder='Treść zadania...',
                            style={
                                'width': '100%',
                                'padding': '10px',
                                'border': f"1px solid {LIGHT_THEME['border']}",
                                'borderRadius': LIGHT_THEME['radius'],
                                'fontSize': '14px',
                                'minHeight': '80px',
                                'marginBottom': '12px',
                                'background': LIGHT_THEME['input_bg'],
                                'resize': 'vertical'
                            }
                        ),
                        
                        html.Label("🏷️ Tagi:", style={
                            'display': 'block',
                            'marginBottom': '6px',
                            'fontWeight': '600',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '14px'
                        }),
                        dcc.Dropdown(
                            id={'type': 'task-tags-dropdown', 'index': task['id']},
                            options=tag_options,
                            multi=True,
                            placeholder="Wybierz tagi...",
                            style={
                                'width': '100%',
                                'marginBottom': '12px',
                                'fontSize': '14px'
                            }
                        ),
                        
                        html.Label("✅ Status:", style={
                            'display': 'block',
                            'marginBottom': '6px',
                            'fontWeight': '600',
                            'color': LIGHT_THEME['text'],
                            'fontSize': '14px'
                        }),
                        dcc.RadioItems(
                            id={'type': 'task-solved-radio', 'index': task['id']},
                            options=[
                                {'label': ' ❌ Nie', 'value': False},
                                {'label': ' ✅ Tak', 'value': True}
                            ],
                            value=False,
                            style={
                                'marginBottom': '16px',
                                'fontSize': '14px',
                                'fontWeight': '500'
                            }
                        )
                    ], style={
                        'padding': '16px',
                        'marginBottom': '16px',
                        'background': 'rgba(255, 255, 255, 0.8)',
                        'borderRadius': LIGHT_THEME['radius'],
                        'border': f"1px solid {LIGHT_THEME['border']}",
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
                    })
                ])
            )
        task_set_data = {
            'current_set': set_id,
            'set_name': set_name if set_name else f"Zestaw zadań {datetime.datetime.now().strftime('%Y-%m-%d')}",
            'tasks': tasks,
            'subject': subject
        }
        return form_children, False, task_set_data

    @app.callback(
        Output('math-tasks-store', 'data'),
        Output('task-set-message', 'children'),
        Output('task-set-store', 'data', allow_duplicate=True),
        Output('task-set-size', 'value'),
        Output('task-set-name', 'value'),
        Output({'type': 'task-name-input', 'index': ALL}, 'value'),
        Output({'type': 'task-content-textarea', 'index': ALL}, 'value'),
        Output({'type': 'task-tags-dropdown', 'index': ALL}, 'value'),
        Output({'type': 'task-solved-radio', 'index': ALL}, 'value'),
        Input('save-task-set-button', 'n_clicks'),
        State({'type': 'task-name-input', 'index': ALL}, 'value'),
        State({'type': 'task-content-textarea', 'index': ALL}, 'value'),
        State({'type': 'task-tags-dropdown', 'index': ALL}, 'value'),
        State({'type': 'task-solved-radio', 'index': ALL}, 'value'),
        State('task-set-store', 'data'),
        State('math-tasks-store', 'data'),
        prevent_initial_call=True
    )
    def save_task_set(n_clicks, all_names, all_contents, all_tags_values, all_solved_values, task_set_data, existing_tasks):
        if n_clicks == 0 or not task_set_data or not task_set_data['tasks']:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        from utils import insert_zestaw, insert_zadanie
        tasks_in_set = task_set_data['tasks']
        updated_tasks = []
        set_name = task_set_data['set_name']
        subject = task_set_data.get('subject', 'matematyka')
        
        zestaw_id = insert_zestaw(set_name, subject)
        
        for i, task in enumerate(tasks_in_set):
            name = all_names[i] if all_names[i] else f"Zadanie {task['number']}"
            content = all_contents[i] if all_contents[i] else ""
            tags = all_tags_values[i] if all_tags_values[i] else []
            solved = all_solved_values[i] if all_solved_values[i] is not None else False
            
            insert_zadanie(zestaw_id, task['number'], name, content, solved, tags)
            
            updated_task = {
                'id': task['id'],
                'number': task['number'],
                'name': name,
                'content': content,
                'tags': tags,
                'solved': solved,
                'created': datetime.datetime.now().isoformat(),
                'set_id': zestaw_id,
                'set_name': set_name,
                'subject': subject
            }
            updated_tasks.append(updated_task)
        
        all_tasks = existing_tasks + updated_tasks
        
        # Clear form
        empty_names = [''] * len(all_names)
        empty_contents = [''] * len(all_contents)
        empty_tags = [[] for _ in all_tags_values]
        empty_solved = [False] * len(all_solved_values)
        
        return (
            all_tasks,
            html.Div([
                html.Div([
                    html.Span("🎉", style={'fontSize': '24px', 'marginRight': '8px'}),
                    html.Span("Sukces!", style={'fontWeight': '800', 'fontSize': '16px'})
                ], style={'marginBottom': '8px'}),
                html.Div("Zestaw zadań został zapisany!", style={'fontSize': '14px'})
            ], style={
                'color': LIGHT_THEME['success'],
                'background': f"{LIGHT_THEME['success']}15",
                'padding': '16px',
                'borderRadius': LIGHT_THEME['radius'],
                'border': f"2px solid {LIGHT_THEME['success']}40",
                'textAlign': 'center'
            }),
            {'tasks': [], 'current_set': None, 'set_name': None, 'subject': 'matematyka'},
            5,
            "",
            empty_names,
            empty_contents,
            empty_tags,
            empty_solved
        )

    @app.callback(
        Output('math-tasks-list', 'children'),
        Input('math-tasks-store', 'data'),
        Input('url', 'pathname'),
        prevent_initial_call=False
    )
    def display_math_tasks(tasks, pathname):
        from layouts import get_math_tasks_list
        zestawy = fetch_all_zestawy()
        all_tasks = []
        for zestaw in zestawy:
            zadania = fetch_zadania_for_zestaw(zestaw['id'])
            for zad in zadania:
                all_tasks.append({
                    'id': zad['id'],
                    'number': zad['nr_zadania'],
                    'name': zad['nazwa'],
                    'content': zad['tresc'],
                    'tags': zad.get('tags', []),
                    'solved': bool(zad['solved']),
                    'created': zad['created_at'].isoformat() if hasattr(zad['created_at'], 'isoformat') else str(zad['created_at']),
                    'set_id': zestaw['id'],
                    'set_name': zestaw['name'],
                    'subject': zestaw.get('subject', 'matematyka')
                })
        return get_math_tasks_list(all_tasks)

    @app.callback(
        [Output('edit-modal', 'style', allow_duplicate=True),
         Output('edit-task-name', 'value'),
         Output('edit-task-content', 'value'),
         Output('edit-task-tags', 'value'),
         Output('edit-task-tags', 'options'),
         Output('edit-task-solved', 'value'),
         Output('edit-task-store', 'data')],
        [Input({'type': 'edit-btn', 'index': ALL}, 'n_clicks'),
         Input('cancel-edit-button', 'n_clicks')],
        [State({'type': 'edit-btn', 'index': ALL}, 'id'),
         State('math-tasks-store', 'data'),
         State('edit-task-store', 'data')],
        prevent_initial_call=True
    )
    def handle_edit_modal(edit_clicks, cancel_clicks, edit_ids, tasks, edit_store):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        trigger_id = ctx.triggered[0]['prop_id']
        
        if 'cancel-edit-button' in trigger_id:
            return {'display': 'none'}, '', '', [], [], False, {}
        
        if 'edit-btn' in trigger_id:
            button_id = eval(trigger_id.split('.')[0])
            task_id = button_id['index']
            task_to_edit = next((task for task in tasks if task['id'] == task_id), None)
            
            if task_to_edit:
                subject = task_to_edit.get('subject', 'matematyka')
                tag_options = [{'label': tag.replace('_', ' '), 'value': tag} for tag in get_tags_for_subject(subject)]
                return (
                    {'display': 'block'},
                    task_to_edit['name'],
                    task_to_edit['content'],
                    task_to_edit['tags'],
                    tag_options,
                    task_to_edit['solved'],
                    {'task_id': task_id}
                )
        
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update

    @app.callback(
        [Output('math-tasks-store', 'data', allow_duplicate=True),
         Output('edit-modal', 'style', allow_duplicate=True),
         Output('edit-task-store', 'data', allow_duplicate=True)],
        Input('save-edit-button', 'n_clicks'),
        [State('edit-task-name', 'value'),
         State('edit-task-content', 'value'),
         State('edit-task-tags', 'value'),
         State('edit-task-solved', 'value'),
         State('edit-task-store', 'data'),
         State('math-tasks-store', 'data')],
        prevent_initial_call=True
    )
    def save_task_edit(n_clicks, name, content, tags, solved, edit_store, tasks):
        if n_clicks == 0 or not edit_store or 'task_id' not in edit_store:
            return no_update, no_update, no_update
        
        task_id = edit_store['task_id']
        updated_tasks = []
        
        for task in tasks:
            if task['id'] == task_id:
                updated_task = task.copy()
                updated_task['name'] = name if name else f"Zadanie {task['number']}"
                updated_task['content'] = content if content else ""
                updated_task['tags'] = tags if tags else []
                updated_task['solved'] = solved if solved is not None else False
                updated_tasks.append(updated_task)
            else:
                updated_tasks.append(task)
        
        return updated_tasks, {'display': 'none'}, {}

    @app.callback(
        Output('math-tasks-store', 'data', allow_duplicate=True),
        Input({'type': 'delete-btn', 'index': ALL}, 'n_clicks'),
        [State({'type': 'delete-btn', 'index': ALL}, 'id'),
         State('math-tasks-store', 'data')],
        prevent_initial_call=True
    )
    def delete_task(delete_clicks, delete_ids, tasks):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        button_info = eval(button_id)
        task_id = button_info['index']
        
        return [task for task in tasks if task['id'] != task_id]

    @app.callback(
        Output('stats-graph-math', 'figure'),
        Output('stats-summary-math', 'children'),
        Input('math-tasks-store', 'data')
    )
    def update_stats_math(tasks):
        zadania = fetch_all_zadania_with_tags()
        math_tasks = [z for z in zadania if z.get('subject', 'matematyka') == 'matematyka']
        
        if not math_tasks:
            import plotly.graph_objects as go
            empty_fig = go.Figure()
            empty_fig.update_layout(
                title='Brak danych do wyświetlenia',
                xaxis={'visible': False},
                yaxis={'visible': False},
                annotations=[{
                    'text': 'Brak danych',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 28}
                }]
            )
            return empty_fig, "Brak danych do wyświetlenia"
        
        tag_stats = calculate_tag_stats(math_tasks, 'matematyka')
        fig = create_radar_chart(tag_stats, 'matematyka')
        summary = create_stats_summary(tag_stats, 'matematyka')
        return fig, summary

    @app.callback(
        Output('stats-graph-it', 'figure'),
        Output('stats-summary-it', 'children'),
        Input('math-tasks-store', 'data')
    )
    def update_stats_it(tasks):
        zadania = fetch_all_zadania_with_tags()
        it_tasks = [z for z in zadania if z.get('subject', 'matematyka') == 'informatyka']
        
        if not it_tasks:
            import plotly.graph_objects as go
            empty_fig = go.Figure()
            empty_fig.update_layout(
                title='Brak danych do wyświetlenia',
                xaxis={'visible': False},
                yaxis={'visible': False},
                annotations=[{
                    'text': 'Brak danych',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 28}
                }]
            )
            return empty_fig, "Brak danych do wyświetlenia"
        
        tag_stats = calculate_tag_stats(it_tasks, 'informatyka')
        fig = create_radar_chart(tag_stats, 'informatyka')
        summary = create_stats_summary(tag_stats, 'informatyka')
        return fig, summary
