# callbacks.py
from dash import dcc, html, Input, Output, State, ALL, MATCH
from dash import callback, no_update
import uuid
import datetime
from utils import (
    fetch_all_zestawy, fetch_zadania_for_zestaw, fetch_all_zadania_with_tags,
    get_tags_for_subject, calculate_tag_stats, create_radar_chart, create_stats_summary,
    update_zadanie, delete_zadanie, fetch_zadanie_by_id, update_zestaw, fetch_zestaw_by_id,
    get_next_task_number, delete_zestaw, insert_zadanie, insert_zestaw,
    get_kategorie_for_zestaw, get_kategorie_by_ids,
    add_new_kategoria, delete_kategoria, get_kategorie_for_subject, 
    clear_all_categories, clear_all_tasks, clear_entire_database
)
from theme import LIGHT_THEME

# --- CALLBACKS ---
def register_callbacks(app):
    from dash import callback_context
    from utils import fetch_all_zestawy, fetch_zadania_for_zestaw, fetch_all_zadania_with_tags

    @app.callback(
        [Output({'type': 'set-dropdown-menu', 'index': ALL}, 'style')],
        [Input({'type': 'toggle-set-menu', 'index': ALL}, 'n_clicks')],
        [State({'type': 'set-dropdown-menu', 'index': ALL}, 'style'),
         State({'type': 'toggle-set-menu', 'index': ALL}, 'id')],
        prevent_initial_call=True
    )
    def handle_dropdown_menus(n_clicks_list, current_styles, button_ids):
        ctx = callback_context
        if not ctx.triggered:
            return [no_update]
        
        trigger = ctx.triggered[0]['prop_id']
        updated_styles = [style.copy() for style in current_styles]
        
        # Toggle konkretnego menu
        if 'toggle-set-menu' in trigger:
            button_info = eval(trigger.split('.')[0])
            button_index = button_info['index']
            
            # Znajdź indeks w liście
            menu_idx = next((i for i, btn_id in enumerate(button_ids) if btn_id['index'] == button_index), None)
            
            if menu_idx is not None and n_clicks_list[menu_idx] > 0:
                if updated_styles[menu_idx]['display'] == 'none':
                    updated_styles[menu_idx]['display'] = 'block'
                else:
                    updated_styles[menu_idx]['display'] = 'none'
        
        return [updated_styles]

    @app.callback(
        Output('page-content', 'children', allow_duplicate=True),
        Input('url', 'pathname'),
        prevent_initial_call=True
    )
    def display_page(pathname):
        from layouts import get_home_layout, get_stats_layout, get_stats_layout_it, get_math_tasks_layout, get_manage_categories_layout
        if pathname == '/':
            return get_home_layout()
        elif pathname == '/math-tasks':
            return get_math_tasks_layout()
        elif pathname == '/stats':
            return get_stats_layout(subject="matematyka")
        elif pathname == '/stats-it':
            return get_stats_layout_it()
        elif pathname == '/manage-categories':
            return get_manage_categories_layout()
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

    # Delete modal visibility and data
    @app.callback(
        [Output('delete-modal', 'style'),
         Output('delete-task-name', 'children'),
         Output('delete-task-tags', 'children'),
         Output('delete-task-status', 'children'),
         Output('delete-task-store', 'data')],
        [Input({'type': 'delete-btn', 'index': ALL}, 'n_clicks'),
         Input('cancel-delete-button', 'n_clicks'),
         Input('confirm-delete-button', 'n_clicks')],
        [State({'type': 'delete-btn', 'index': ALL}, 'id')],
        prevent_initial_call=True
    )
    def toggle_delete_modal(delete_clicks, cancel_clicks, confirm_clicks, delete_ids):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update
        
        trigger = ctx.triggered[0]['prop_id']
        
        if 'cancel-delete-button' in trigger or 'confirm-delete-button' in trigger:
            return {'display': 'none'}, '', '', '', {}
        
        if 'delete-btn' in trigger and any(delete_clicks):
            # Get the task ID from the button that was clicked
            button_id = eval(trigger.split('.')[0])
            task_id = button_id['index']
            
            # Fetch task details from database
            task = fetch_zadanie_by_id(task_id)
            if task:
                task_name = task['nazwa'] or f"Zadanie {task['nr_zadania']}"
                task_tags = ', '.join(task['tags']) if task['tags'] else 'Brak tagów'
                task_status = "✅ Rozwiązane" if task['solved'] else "❌ Nierozwiązane"
                
                return (
                    {'display': 'block'},
                    task_name,
                    task_tags,
                    task_status,
                    {'task_id': task_id, 'db_id': task['id']}
                )
        
        return {'display': 'none'}, '', '', '', {}

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
        
        # Najpierw utwórz zestaw w bazie, żeby mieć ID
        zestaw_id = insert_zestaw(set_name if set_name else f"Zestaw zadań {datetime.datetime.now().strftime('%Y-%m-%d')}", subject)
        
        # Nie tworzymy już domyślnych kategorii - użytkownik dodaje własne
        
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
        
        # Pobierz kategorie dla tego zestawu
        kategorie = get_kategorie_for_zestaw(zestaw_id)
        tag_options = [{'label': k['nazwa'], 'value': k['id']} for k in kategorie]
        
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
                        
                        html.Label("🏷️ Kategorie:", style={
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
                            placeholder="Wybierz kategorie...",
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
            'current_set': zestaw_id,  # Używaj prawdziwego ID z bazy
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
        
        tasks_in_set = task_set_data['tasks']
        updated_tasks = []
        set_name = task_set_data['set_name']
        subject = task_set_data.get('subject', 'matematyka')
        
        zestaw_id = task_set_data['current_set']  # Używaj istniejącego ID
        
        for i, task in enumerate(tasks_in_set):
            name = all_names[i] if all_names[i] else f"Zadanie {task['number']}"
            content = all_contents[i] if all_contents[i] else ""
            kategorie_ids = all_tags_values[i] if all_tags_values[i] else []
            solved = all_solved_values[i] if all_solved_values[i] is not None else False
            
            insert_zadanie(zestaw_id, task['number'], name, content, solved, kategorie_ids)
            
            # Pobierz nazwy kategorii dla wyświetlania
            kategorie = get_kategorie_for_zestaw(zestaw_id)
            category_names = [k['nazwa'] for k in kategorie if k['id'] in kategorie_ids]
            
            updated_task = {
                'id': task['id'],
                'number': task['number'],
                'name': name,
                'content': content,
                'tags': category_names,
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
            
            # Fetch task from database instead of store
            task_to_edit = fetch_zadanie_by_id(task_id)
            
            if task_to_edit:
                # Pobierz kategorie dla tego zestawu
                kategorie = get_kategorie_for_zestaw(task_to_edit['id_zestawu'])
                tag_options = [{'label': k['nazwa'], 'value': k['id']} for k in kategorie]
                
                return (
                    {'display': 'block'},
                    task_to_edit['nazwa'],
                    task_to_edit['tresc'],
                    task_to_edit.get('kategorie_ids', []),
                    tag_options,
                    task_to_edit['solved'],
                    {'task_id': task_id, 'db_id': task_to_edit['id']}
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
    def save_task_edit(n_clicks, name, content, kategorie_ids, solved, edit_store, tasks):
        if n_clicks == 0 or not edit_store or 'db_id' not in edit_store:
            return no_update, no_update, no_update
        
        db_id = edit_store['db_id']
        
        # Update in database
        update_zadanie(db_id, name, content, kategorie_ids, solved)
        
        # Update in store (for immediate UI update)
        task_id = edit_store['task_id']
        updated_tasks = []
        
        for task in tasks:
            if task['id'] == task_id:
                updated_task = task.copy()
                updated_task['name'] = name if name else f"Zadanie {task['number']}"
                updated_task['content'] = content if content else ""
                
                # Pobierz nazwy kategorii dla wyświetlania
                if kategorie_ids:
                    # Pobierz zestaw_id z zadania
                    zadanie_db = fetch_zadanie_by_id(db_id)
                    if zadanie_db:
                        kategorie = get_kategorie_for_zestaw(zadanie_db['id_zestawu'])
                        updated_task['tags'] = [k['nazwa'] for k in kategorie if k['id'] in kategorie_ids]
                    else:
                        updated_task['tags'] = []
                else:
                    updated_task['tags'] = []
                
                updated_task['solved'] = solved if solved is not None else False
                updated_tasks.append(updated_task)
            else:
                updated_tasks.append(task)
        
        return updated_tasks, {'display': 'none'}, {}

    # Delete task with database operation
    @app.callback(
        [Output('math-tasks-store', 'data', allow_duplicate=True),
         Output('delete-modal', 'style', allow_duplicate=True),
         Output('delete-task-store', 'data', allow_duplicate=True)],
        Input('confirm-delete-button', 'n_clicks'),
        [State('delete-task-store', 'data'),
         State('math-tasks-store', 'data')],
        prevent_initial_call=True
    )
    def confirm_delete_task(n_clicks, delete_store, tasks):
        if n_clicks == 0 or not delete_store or 'db_id' not in delete_store:
            return no_update, no_update, no_update
        
        db_id = delete_store['db_id']
        task_id = delete_store['task_id']
        
        # Delete from database
        delete_zadanie(db_id)
        
        # Remove from store (for immediate UI update)
        updated_tasks = [task for task in tasks if task['id'] != task_id]
        
        return updated_tasks, {'display': 'none'}, {}

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

    # Edit set modal visibility
    @app.callback(
        [Output('edit-set-modal', 'style'),
         Output('edit-set-name', 'value'),
         Output('edit-set-subject', 'value'),
         Output('edit-set-store', 'data')],
        [Input({'type': 'edit-set-btn', 'index': ALL}, 'n_clicks'),
         Input('cancel-edit-set-button', 'n_clicks'),
         Input('save-edit-set-button', 'n_clicks')],
        [State({'type': 'edit-set-btn', 'index': ALL}, 'id')],
        prevent_initial_call=True
    )
    def handle_edit_set_modal(edit_clicks, cancel_clicks, save_clicks, edit_ids):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update
        
        trigger_id = ctx.triggered[0]['prop_id']
        
        if 'cancel-edit-set-button' in trigger_id or 'save-edit-set-button' in trigger_id:
            return {'display': 'none'}, '', 'matematyka', {}
        
        if 'edit-set-btn' in trigger_id and any(edit_clicks):
            button_id = eval(trigger_id.split('.')[0])
            set_id = button_id['index']
            
            # Fetch set from database
            zestaw = fetch_zestaw_by_id(set_id)
            
            if zestaw:
                return (
                    {'display': 'block'},
                    zestaw['name'],
                    zestaw.get('subject', 'matematyka'),
                    {'set_id': set_id}
                )
        
        return no_update, no_update, no_update, no_update

    # Save set edit
    @app.callback(
        [Output('math-tasks-store', 'data', allow_duplicate=True),
         Output('edit-set-modal', 'style', allow_duplicate=True),
         Output('edit-set-store', 'data', allow_duplicate=True)],
        Input('save-edit-set-button', 'n_clicks'),
        [State('edit-set-name', 'value'),
         State('edit-set-subject', 'value'),
         State('edit-set-store', 'data'),
         State('math-tasks-store', 'data')],
        prevent_initial_call=True
    )
    def save_set_edit(n_clicks, name, subject, edit_store, tasks):
        if n_clicks == 0 or not edit_store or 'set_id' not in edit_store:
            return no_update, no_update, no_update
        
        set_id = edit_store['set_id']
        
        # Update in database
        update_zestaw(set_id, name, subject)
        
        # Update tasks in store
        updated_tasks = []
        for task in tasks:
            if task.get('set_id') == set_id:
                updated_task = task.copy()
                updated_task['set_name'] = name
                updated_task['subject'] = subject
                updated_tasks.append(updated_task)
            else:
                updated_tasks.append(task)
        
        return updated_tasks, {'display': 'none'}, {}

    # Add task to set modal visibility and setup
    @app.callback(
        [Output('add-task-to-set-modal', 'style'),
         Output('add-task-set-name-display', 'children'),
         Output('add-task-tags', 'options'),
         Output('add-task-to-set-store', 'data'),
         Output('add-task-name', 'value'),
         Output('add-task-content', 'value'),
         Output('add-task-tags', 'value'),
         Output('add-task-solved', 'value')],
        [Input({'type': 'add-task-to-set-btn', 'index': ALL}, 'n_clicks'),
         Input('cancel-add-task-button', 'n_clicks'),
         Input('save-add-task-button', 'n_clicks')],
        [State({'type': 'add-task-to-set-btn', 'index': ALL}, 'id')],
        prevent_initial_call=True
    )
    def handle_add_task_to_set_modal(add_clicks, cancel_clicks, save_clicks, add_ids):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        trigger_id = ctx.triggered[0]['prop_id']
        
        if 'cancel-add-task-button' in trigger_id or 'save-add-task-button' in trigger_id:
            return {'display': 'none'}, '', [], {}, '', '', [], False
        
        if 'add-task-to-set-btn' in trigger_id and any(add_clicks):
            button_id = eval(trigger_id.split('.')[0])
            set_id = button_id['index']
            
            # Fetch set info
            zestaw = fetch_zestaw_by_id(set_id)
            
            if zestaw:
                subject = zestaw.get('subject', 'matematyka')
                kategorie = get_kategorie_for_zestaw(set_id)
                tag_options = [{'label': k['nazwa'], 'value': k['id']} for k in kategorie]
                next_number = get_next_task_number(set_id)
                
                return (
                    {'display': 'block'},
                    f"📚 Zestaw: {zestaw['name']} | 🔢 Numer zadania: {next_number}",
                    tag_options,
                    {'set_id': set_id, 'set_name': zestaw['name'], 'subject': subject, 'next_number': next_number},
                    '',
                    '',
                    [],
                    False
                )
        
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # Save new task to existing set
    @app.callback(
        [Output('math-tasks-store', 'data', allow_duplicate=True),
         Output('add-task-to-set-modal', 'style', allow_duplicate=True),
         Output('add-task-to-set-store', 'data', allow_duplicate=True),
         Output('add-task-name', 'value', allow_duplicate=True),
         Output('add-task-content', 'value', allow_duplicate=True),
         Output('add-task-tags', 'value', allow_duplicate=True),
         Output('add-task-solved', 'value', allow_duplicate=True)],
        Input('save-add-task-button', 'n_clicks'),
        [State('add-task-name', 'value'),
         State('add-task-content', 'value'),
         State('add-task-tags', 'value'),
         State('add-task-solved', 'value'),
         State('add-task-to-set-store', 'data'),
         State('math-tasks-store', 'data')],
        prevent_initial_call=True
    )
    def save_new_task_to_set(n_clicks, name, content, kategorie_ids, solved, add_store, tasks):
        if n_clicks == 0 or not add_store or 'set_id' not in add_store:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        set_id = add_store['set_id']
        set_name = add_store['set_name']
        subject = add_store['subject']
        task_number = add_store['next_number']
        
        # Default values
        task_name = name if name else f"Zadanie {task_number}"
        task_content = content if content else ""
        task_kategorie_ids = kategorie_ids if kategorie_ids else []
        task_solved = solved if solved is not None else False
        
        # Insert into database
        insert_zadanie(set_id, task_number, task_name, task_content, task_solved, task_kategorie_ids)
        
        # Pobierz nazwy kategorii dla wyświetlania
        if task_kategorie_ids:
            kategorie = get_kategorie_by_ids(task_kategorie_ids)
            task_tags = [k['nazwa'] for k in kategorie]
        else:
            task_tags = []
        
        # Create new task for store
        new_task = {
            'id': str(uuid.uuid4()),
            'number': task_number,
            'name': task_name,
            'content': task_content,
            'tags': task_tags,
            'solved': task_solved,
            'created': datetime.datetime.now().isoformat(),
            'set_id': set_id,
            'set_name': set_name,
            'subject': subject
        }
        
        # Add to existing tasks
        updated_tasks = tasks + [new_task]
        
        return (
            updated_tasks,
            {'display': 'none'},
            {},
            '',
            '',
            [],
            False
        )

    @app.callback(
        Output('math-tasks-store', 'data', allow_duplicate=True),
        Input({'type': 'delete-set-btn', 'index': ALL}, 'n_clicks'),
        [State({'type': 'delete-set-btn', 'index': ALL}, 'id'),
         State('math-tasks-store', 'data')],
        prevent_initial_call=True
    )
    def delete_task_set(delete_clicks, delete_ids, tasks):
        ctx = callback_context
        if not ctx.triggered or not any(delete_clicks):
            return no_update
        
        button_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        set_id = button_id['index']
        
        # Delete from database
        delete_zestaw(set_id)
        
        # Remove from store
        updated_tasks = [task for task in tasks if task.get('set_id') != set_id]

        return updated_tasks

    # === CATEGORIES MANAGEMENT CALLBACKS ===
    
    # Add new category
    @app.callback(
        Output('category-message', 'children'),
        [Input('add-category-button', 'n_clicks')],
        [State('category-subject-dropdown', 'value'),
         State('new-category-name', 'value')]
    )
    def add_new_category_callback(n_clicks, subject, category_name):
        if not n_clicks or not subject or not category_name:
            return ""
        
        # Add category
        result = add_new_kategoria(category_name.strip(), subject)
        
        if result is None:
            return html.Div("⚠️ Kategoria już istnieje dla tego przedmiotu", style={'color': LIGHT_THEME['warning']})
        else:
            return html.Div("✅ Pomyślnie dodano kategorię", style={'color': LIGHT_THEME['success']})

    # Display categories list
    @app.callback(
        Output('categories-list', 'children'),
        [Input('url', 'pathname'),
         Input('filter-subject-dropdown', 'value'),
         Input('category-message', 'children')]  # Refresh when category is added
    )
    def display_categories_list(pathname, filter_subject, _):
        if pathname != '/manage-categories':
            return ""
        
        # Get categories based on filter
        if filter_subject == 'all' or not filter_subject:
            # Get all categories for both subjects
            all_categories = []
            for subject in ['matematyka', 'informatyka']:
                categories = get_kategorie_for_subject(subject)
                all_categories.extend(categories)
        else:
            # Get categories for specific subject
            all_categories = get_kategorie_for_subject(filter_subject)
        
        if not all_categories:
            return html.Div([
                html.Div("📭", style={'fontSize': '64px', 'textAlign': 'center', 'marginBottom': '16px'}),
                html.P("Brak kategorii do wyświetlenia", style={
                    'textAlign': 'center',
                    'color': LIGHT_THEME['placeholder'],
                    'fontSize': '18px',
                    'fontWeight': '500'
                })
            ], style={'padding': '40px'})
        
        # Create category cards
        category_cards = []
        for cat in all_categories:
            category_cards.append(
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4(cat['nazwa'], style={
                                'margin': '0',
                                'color': LIGHT_THEME['text'],
                                'fontWeight': '700',
                                'fontSize': '18px'
                            }),
                            html.P(f"Przedmiot: {cat.get('subject', 'N/A').capitalize()}", style={
                                'margin': '0',
                                'color': LIGHT_THEME['placeholder'],
                                'fontSize': '14px'
                            })
                        ], style={'flex': '1'}),
                        
                        html.Button([
                            html.Span("🗑️", style={'fontSize': '16px'})
                        ],
                        id={'type': 'delete-category-btn', 'index': cat['id']},
                        n_clicks=0,
                        style={
                            'background': LIGHT_THEME['error'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '6px',
                            'width': '40px',
                            'height': '40px',
                            'cursor': 'pointer',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'transition': 'all 0.3s ease'
                        })
                    ], style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'space-between'
                    })
                ], style={
                    'background': 'white',
                    'padding': '20px',
                    'borderRadius': LIGHT_THEME['radius'],
                    'boxShadow': LIGHT_THEME['shadow'],
                    'marginBottom': '16px',
                    'border': f"1px solid {LIGHT_THEME['border']}"
                })
            )
        
        return category_cards

    # Delete category
    @app.callback(
        Output('categories-list', 'children', allow_duplicate=True),
        Input({'type': 'delete-category-btn', 'index': ALL}, 'n_clicks'),
        [State('filter-subject-dropdown', 'value')],
        prevent_initial_call=True
    )
    def delete_category_callback(delete_clicks, filter_subject):
        ctx = callback_context
        if not ctx.triggered or not any(delete_clicks):
            return no_update
        
        button_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        category_id = button_id['index']
        
        # Delete from database
        success = delete_kategoria(category_id)
        
        if not success:
            return no_update
        
        # Return updated list (same logic as display_categories_list)
        if filter_subject == 'all' or not filter_subject:
            # Get all categories for both subjects
            all_categories = []
            for subject in ['matematyka', 'informatyka']:
                categories = get_kategorie_for_subject(subject)
                all_categories.extend(categories)
        else:
            # Get categories for specific subject
            all_categories = get_kategorie_for_subject(filter_subject)
        
        if not all_categories:
            return html.Div([
                html.Div("📭", style={'fontSize': '64px', 'textAlign': 'center', 'marginBottom': '16px'}),
                html.P("Brak kategorii do wyświetlenia", style={
                    'textAlign': 'center',
                    'color': LIGHT_THEME['placeholder'],
                    'fontSize': '18px',
                    'fontWeight': '500'
                })
            ], style={'padding': '40px'})
        
        category_cards = []
        for cat in all_categories:
            category_cards.append(
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4(cat['nazwa'], style={
                                'margin': '0',
                                'color': LIGHT_THEME['text'],
                                'fontWeight': '700',
                                'fontSize': '18px'
                            }),
                            html.P(f"Przedmiot: {cat.get('subject', 'N/A').capitalize()}", style={
                                'margin': '0',
                                'color': LIGHT_THEME['placeholder'],
                                'fontSize': '14px'
                            })
                        ], style={'flex': '1'}),
                        
                        html.Button([
                            html.Span("🗑️", style={'fontSize': '16px'})
                        ],
                        id={'type': 'delete-category-btn', 'index': cat['id']},
                        n_clicks=0,
                        style={
                            'background': LIGHT_THEME['error'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '6px',
                            'width': '40px',
                            'height': '40px',
                            'cursor': 'pointer',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'transition': 'all 0.3s ease'
                        })
                    ], style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'space-between'
                    })
                ], style={
                    'background': 'white',
                    'padding': '20px',
                    'borderRadius': LIGHT_THEME['radius'],
                    'boxShadow': LIGHT_THEME['shadow'],
                    'marginBottom': '16px',
                    'border': f"1px solid {LIGHT_THEME['border']}"
                })
            )
        
        return category_cards
    # Clear all categories
    @app.callback(
        [Output("category-message", "children", allow_duplicate=True),
         Output("categories-list", "children", allow_duplicate=True)],
        Input("clear-all-categories-button", "n_clicks"),
        prevent_initial_call=True
    )
    def clear_all_categories_callback(n_clicks):
        if not n_clicks:
            return no_update, no_update
        
        # Clear all categories from database
        rows_affected = clear_all_categories()
        
        message = html.Div(f"✅ Usunięto {rows_affected} kategorii z bazy danych", 
                          style={"color": LIGHT_THEME["success"]})
        
        empty_list = html.Div([
            html.Div("📭", style={"fontSize": "64px", "textAlign": "center", "marginBottom": "16px"}),
            html.P("Brak kategorii do wyświetlenia", style={
                "textAlign": "center",
                "color": LIGHT_THEME["placeholder"],
                "fontSize": "18px",
                "fontWeight": "500"
            })
        ], style={"padding": "40px"})
        
        return message, empty_list
    # === ADMIN PANEL CALLBACKS ===
    
    # Global keyboard listener for admin panel
    @app.callback(
        Output('admin-panel-modal', 'style'),
        Input('keyboard-store', 'data'),
        State('admin-panel-modal', 'style')
    )
    def toggle_admin_panel(keyboard_data, current_style):
        # Check for Ctrl+Shift+A combination
        keys = keyboard_data.get('keys', [])
        if len(keys) >= 3 and 'Control' in keys and 'Shift' in keys and 'KeyA' in keys:
            if current_style.get('display') == 'none':
                return {'display': 'flex'}
        return current_style
    
    # Close admin panel
    @app.callback(
        Output('admin-panel-modal', 'style', allow_duplicate=True),
        Input('close-admin-panel-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def close_admin_panel(n_clicks):
        if n_clicks:
            return {'display': 'none'}
        return no_update
    
    # Admin clear categories
    @app.callback(
        Output('admin-message', 'children'),
        [Input('admin-clear-categories-button', 'n_clicks'),
         Input('admin-clear-tasks-button', 'n_clicks'),
         Input('admin-clear-all-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def admin_clear_operations(clear_categories_clicks, clear_tasks_clicks, clear_all_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return ""
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        try:
            if button_id == 'admin-clear-categories-button' and clear_categories_clicks:
                rows_affected = clear_all_categories()
                return html.Div(f"✅ Usunięto {rows_affected} kategorii z bazy danych", 
                              style={'color': LIGHT_THEME['success']})
                              
            elif button_id == 'admin-clear-tasks-button' and clear_tasks_clicks:
                success = clear_all_tasks()
                if success:
                    return html.Div("✅ Usunięto wszystkie zadania i zestawy z bazy danych", 
                                  style={'color': LIGHT_THEME['success']})
                else:
                    return html.Div("❌ Błąd podczas usuwania zadań", 
                                  style={'color': LIGHT_THEME['error']})
                                  
            elif button_id == 'admin-clear-all-button' and clear_all_clicks:
                success = clear_entire_database()
                if success:
                    return html.Div("💣 Wyczyszczono całą bazę danych!", 
                                  style={'color': LIGHT_THEME['error'], 'fontWeight': 'bold'})
                else:
                    return html.Div("❌ Błąd podczas czyszczenia bazy danych", 
                                  style={'color': LIGHT_THEME['error']})
                                  
        except Exception as e:
            return html.Div(f"❌ Błąd: {str(e)}", 
                          style={'color': LIGHT_THEME['error']})
        
        return ""
