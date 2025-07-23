# --- DB UTILS ---
import mariadb

def get_db_connection():
    return mariadb.connect(
        user="root",
        password="0000",
        host="localhost",
        port=3306,
        database="matura_app"
    )

def insert_zestaw(name, subject):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO zestaw_matura (created_at, name, subject)
        VALUES (NOW(), ?, ?)
        """,
        (name, subject)
    )
    conn.commit()
    zestaw_id = cur.lastrowid
    cur.close()
    conn.close()
    return zestaw_id

def insert_zadanie(id_zestawu, nr_zadania, nazwa, tresc, solved, kategorie_ids):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Zadanie (id_zestawu, nr_zadania, nazwa, tresc, solved, created_at)
        VALUES (?, ?, ?, ?, ?, NOW())
        """,
        (id_zestawu, nr_zadania, nazwa, tresc, int(solved))
    )
    zadanie_id = cur.lastrowid
    
    # Dodaj powiązania z kategoriami
    for kategoria_id in kategorie_ids:
        cur.execute(
            "INSERT INTO zadanie_kategoria (zadanie_id, kategoria_id) VALUES (?, ?)",
            (zadanie_id, kategoria_id)
        )
    
    conn.commit()
    cur.close()
    conn.close()

def update_zadanie(zadanie_id, nazwa, tresc, kategorie_ids, solved):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Zadanie 
        SET nazwa = ?, tresc = ?, solved = ?
        WHERE id = ?
        """,
        (nazwa, tresc, int(solved), zadanie_id)
    )
    
    # Usuń stare powiązania z kategoriami
    cur.execute("DELETE FROM zadanie_kategoria WHERE zadanie_id = ?", (zadanie_id,))
    
    # Dodaj nowe powiązania z kategoriami
    for kategoria_id in kategorie_ids:
        cur.execute(
            "INSERT INTO zadanie_kategoria (zadanie_id, kategoria_id) VALUES (?, ?)",
            (zadanie_id, kategoria_id)
        )
    
    conn.commit()
    cur.close()
    conn.close()

def delete_zadanie(zadanie_id):
    """Delete a task from the database"""
    conn = get_db_connection()
    cur = conn.cursor()
    # Usuń powiązania z kategoriami
    cur.execute("DELETE FROM zadanie_kategoria WHERE zadanie_id = ?", (zadanie_id,))
    # Usuń zadanie
    cur.execute("DELETE FROM Zadanie WHERE id = ?", (zadanie_id,))
    conn.commit()
    rows_affected = cur.rowcount
    cur.close()
    conn.close()
    return rows_affected > 0

def fetch_zadanie_by_id(zadanie_id):
    """Fetch a single task by ID"""
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT z.*, GROUP_CONCAT(k.nazwa) as kategorie_nazwy, GROUP_CONCAT(k.id) as kategorie_ids
        FROM Zadanie z
        LEFT JOIN zadanie_kategoria zk ON z.id = zk.zadanie_id
        LEFT JOIN kategoria k ON zk.kategoria_id = k.id
        WHERE z.id = ?
        GROUP BY z.id
    """, (zadanie_id,))
    zadanie = cur.fetchone()
    if zadanie:
        zadanie['tags'] = [t.strip() for t in zadanie.get('kategorie_nazwy', '').split(',')] if zadanie.get('kategorie_nazwy') else []
        zadanie['kategorie_ids'] = [int(t.strip()) for t in zadanie.get('kategorie_ids', '').split(',')] if zadanie.get('kategorie_ids') else []
        zadanie['solved'] = bool(zadanie['solved'])
    cur.close()
    conn.close()
    return zadanie

def fetch_all_zestawy():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM zestaw_matura ORDER BY created_at DESC")
    zestawy = cur.fetchall()
    cur.close()
    conn.close()
    return zestawy

def fetch_zadania_for_zestaw(zestaw_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT z.*, GROUP_CONCAT(k.nazwa) as kategorie_nazwy, GROUP_CONCAT(k.id) as kategorie_ids
        FROM Zadanie z
        LEFT JOIN zadanie_kategoria zk ON z.id = zk.zadanie_id
        LEFT JOIN kategoria k ON zk.kategoria_id = k.id
        WHERE z.id_zestawu = ?
        GROUP BY z.id
        ORDER BY z.nr_zadania ASC
    """, (zestaw_id,))
    zadania = cur.fetchall()
    for zad in zadania:
        zad['tags'] = [t.strip() for t in zad.get('kategorie_nazwy', '').split(',')] if zad.get('kategorie_nazwy') else []
        zad['kategorie_ids'] = [int(t.strip()) for t in zad.get('kategorie_ids', '').split(',')] if zad.get('kategorie_ids') else []
        zad['solved'] = bool(zad['solved'])
    cur.close()
    conn.close()
    return zadania

def fetch_all_zadania_with_tags():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            z.id as id,
            z.nr_zadania as number,
            z.nazwa as name,
            z.tresc as content,
            z.solved as solved,
            z.created_at as created,
            z.id_zestawu as set_id,
            zm.name as set_name,
            zm.subject as subject,
            GROUP_CONCAT(k.nazwa) as kategorie_nazwy,
            GROUP_CONCAT(k.id) as kategorie_ids
        FROM Zadanie z
        LEFT JOIN zestaw_matura zm ON z.id_zestawu = zm.id
        LEFT JOIN zadanie_kategoria zk ON z.id = zk.zadanie_id
        LEFT JOIN kategoria k ON zk.kategoria_id = k.id
        GROUP BY z.id
        ORDER BY z.created_at DESC
    """)
    zadania = cur.fetchall()
    for zad in zadania:
        zad['tags'] = [t.strip() for t in zad.get('kategorie_nazwy', '').split(',')] if zad.get('kategorie_nazwy') else []
        zad['kategorie_ids'] = [int(t.strip()) for t in zad.get('kategorie_ids', '').split(',')] if zad.get('kategorie_ids') else []
        zad['solved'] = bool(zad['solved'])
        if 'subject' not in zad or not zad['subject']:
            zad['subject'] = 'matematyka'
    cur.close()
    conn.close()
    return zadania

def update_zestaw(zestaw_id, name, subject):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE zestaw_matura 
        SET name = ?, subject = ?
        WHERE id = ?
        """,
        (name, subject, zestaw_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def fetch_zestaw_by_id(zestaw_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM zestaw_matura WHERE id = ?", (zestaw_id,))
    zestaw = cur.fetchone()
    cur.close()
    conn.close()
    return zestaw

def get_next_task_number(zestaw_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(nr_zadania) FROM Zadanie WHERE id_zestawu = ?", (zestaw_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return (result[0] + 1) if result[0] else 1

def delete_zestaw(zestaw_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Usuń powiązania zadań z kategoriami
    cur.execute("""
        DELETE zk FROM zadanie_kategoria zk
        JOIN Zadanie z ON zk.zadanie_id = z.id
        WHERE z.id_zestawu = ?
    """, (zestaw_id,))
    # Usuń wszystkie zadania z zestawu
    cur.execute("DELETE FROM Zadanie WHERE id_zestawu = ?", (zestaw_id,))
    # Nie usuwamy kategorii - teraz są przypisane do przedmiotu, nie zestawu
    # Usuń sam zestaw
    cur.execute("DELETE FROM zestaw_matura WHERE id = ?", (zestaw_id,))
    conn.commit()
    cur.close()
    conn.close()

# utils.py
from theme import LIGHT_THEME
import math
from dash import html

def get_tags_for_subject(subject):
    """Pobierz nazwy kategorii dla danego przedmiotu"""
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT DISTINCT nazwa FROM kategoria WHERE subject = ?", (subject,))
    kategorie = cur.fetchall()
    cur.close()
    conn.close()
    return [k['nazwa'] for k in kategorie]

def calculate_tag_stats(tasks, subject):
    tag_stats = {}
    # Pobierz wszystkie kategorie dla danego przedmiotu
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT DISTINCT nazwa FROM kategoria WHERE subject = ?", (subject,))
    kategorie = cur.fetchall()
    cur.close()
    conn.close()
    
    tags = [k['nazwa'] for k in kategorie]
    
    for tag in tags:
        total = 0
        solved = 0
        for task in tasks:
            if task.get('subject', 'matematyka') == subject and tag in task.get('tags', []):
                total += 1
                if task['solved']:
                    solved += 1
        success_rate = solved / total if total > 0 else 0
        tag_stats[tag] = {
            'total': total,
            'solved': solved,
            'success_rate': success_rate
        }
    return tag_stats

def create_radar_chart(tag_stats, subject):
    import plotly.graph_objects as go
    
    tags = get_tags_for_subject(subject)
    
    if not tags:
        # Jeśli brak kategorii, zwróć pusty wykres
        fig = go.Figure()
        fig.update_layout(
            title=f'Brak kategorii dla przedmiotu: {subject.capitalize()}',
            xaxis={'visible': False},
            yaxis={'visible': False},
            annotations=[{
                'text': 'Brak kategorii',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 28}
            }]
        )
        return fig
    
    num_tags = len(tags)
    values = [tag_stats.get(tag, {'success_rate': 0})['success_rate'] for tag in tags]
    values += values[:1]
    
    # Create beautiful gradient colors for the chart
    colors = [
        '#667eea', '#764ba2', '#f093fb', '#f5576c', '#a8edea',
        '#fed6e3', '#d299c2', '#fef9d7', '#667eea', '#764ba2', '#f093fb'
    ]
    
    fig = go.Figure()
    
    # Background circle
    fig.add_trace(go.Scatterpolar(
        r=[1] * (num_tags + 1),
        theta=tags + [tags[0]],
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.05)',
        line=dict(color='rgba(102, 126, 234, 0.1)', width=1),
        name='Zakres maksymalny',
        hoverinfo='none',
        showlegend=False
    ))
    
    # Main data trace with gradient effect
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=tags + [tags[0]],
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.2)',
        line=dict(color='#667eea', width=3),
        name='Twój postęp',
        hovertemplate='<b>%{theta}</b><br>Skuteczność: %{r:.1%}<extra></extra>'
    ))
    
    # Individual points with different colors
    for i, tag in enumerate(tags):
        color = colors[i % len(colors)]
        tag_data = tag_stats.get(tag, {'solved': 0, 'total': 0, 'success_rate': 0})
        fig.add_trace(go.Scatterpolar(
            r=[values[i]],
            theta=[tag],
            mode='markers',
            marker=dict(
                size=15,
                color=color,
                opacity=0.9,
                line=dict(width=3, color='white'),
                symbol='circle'
            ),
            name=tag,
            text=f"{tag}<br>Rozwiązane: {tag_data['solved']}/{tag_data['total']}<br>Skuteczność: {tag_data['success_rate']*100:.1f}%",
            hoverinfo='text',
            showlegend=False
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 1], 
                showticklabels=True,
                tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],
                ticktext=['20%', '40%', '60%', '80%', '100%'],
                tickfont=dict(size=12, color=LIGHT_THEME['text']),
                gridcolor='rgba(102, 126, 234, 0.1)',
                linecolor='rgba(102, 126, 234, 0.2)'
            ),
            angularaxis=dict(
                rotation=90, 
                direction='clockwise',
                tickfont=dict(size=13, color=LIGHT_THEME['text'], family=LIGHT_THEME['font']),
                gridcolor='rgba(102, 126, 234, 0.1)',
                linecolor='rgba(102, 126, 234, 0.2)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        title={
            'text': f'🎯 Poziom opanowania materiału ({subject.capitalize()})',
            'x': 0.5,
            'font': {
                'size': 24,
                'color': LIGHT_THEME['text'],
                'family': LIGHT_THEME['font'],
                'weight': 700
            }
        },
        margin=dict(l=60, r=60, t=80, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family=LIGHT_THEME['font'],
            size=12,
            color=LIGHT_THEME['text']
        ),
        height=600
    )
    return fig

def create_stats_summary(tag_stats, subject):
    tags = get_tags_for_subject(subject)
    
    if not tags:
        return html.Div("Brak kategorii do wyświetlenia", style={
            'textAlign': 'center',
            'padding': '40px',
            'fontSize': '18px',
            'color': LIGHT_THEME['placeholder']
        })
    
    # Filtruj tylko kategorie z danymi
    tags_with_data = [tag for tag in tags if tag_stats.get(tag, {'total': 0})['total'] > 0]
    
    if not tags_with_data:
        return html.Div("Brak danych do wyświetlenia", style={
            'textAlign': 'center',
            'padding': '40px',
            'fontSize': '18px',
            'color': LIGHT_THEME['placeholder']
        })
    
    sorted_tags = sorted(tags_with_data, key=lambda x: tag_stats.get(x, {'success_rate': 0})['success_rate'], reverse=True)
    
    # Calculate overall statistics
    total_tasks = sum(tag_stats.get(tag, {'total': 0})['total'] for tag in tags_with_data)
    total_solved = sum(tag_stats.get(tag, {'solved': 0})['solved'] for tag in tags_with_data)
    overall_success = total_solved / total_tasks if total_tasks > 0 else 0
    
    # Get best and worst performing tags
    best_tags = sorted_tags[:3]
    worst_tags = sorted_tags[-3:]
    worst_tags.reverse()  # Show worst first
    
    summary = html.Div([
        # Overall stats header
        html.Div([
            html.H3("📊 Podsumowanie wyników", style={
                'marginBottom': '20px', 
                'fontWeight': '800',
                'color': LIGHT_THEME['text'],
                'fontSize': '28px',
                'textAlign': 'center'
            }),
            html.Div([
                html.Div([
                    html.Div("🎯", style={'fontSize': '32px', 'marginBottom': '8px'}),
                    html.H4(f"{overall_success*100:.1f}%", style={
                        'margin': '0',
                        'fontSize': '32px',
                        'fontWeight': '800',
                        'color': LIGHT_THEME['success'] if overall_success > 0.6 else LIGHT_THEME['warning'] if overall_success > 0.3 else LIGHT_THEME['error']
                    }),
                    html.P("Ogólna skuteczność", style={
                        'margin': '4px 0 0 0',
                        'fontSize': '14px',
                        'color': LIGHT_THEME['placeholder'],
                        'fontWeight': '500'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '20px',
                    'background': 'linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%)',
                    'borderRadius': LIGHT_THEME['radius'],
                    'flex': '1',
                    'margin': '0 10px'
                }),
                html.Div([
                    html.Div("📝", style={'fontSize': '32px', 'marginBottom': '8px'}),
                    html.H4(f"{total_solved}/{total_tasks}", style={
                        'margin': '0',
                        'fontSize': '32px',
                        'fontWeight': '800',
                        'color': LIGHT_THEME['text']
                    }),
                    html.P("Zadania rozwiązane", style={
                        'margin': '4px 0 0 0',
                        'fontSize': '14px',
                        'color': LIGHT_THEME['placeholder'],
                        'fontWeight': '500'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '20px',
                    'background': 'linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%)',
                    'borderRadius': LIGHT_THEME['radius'],
                    'flex': '1',
                    'margin': '0 10px'
                }),
                html.Div([
                    html.Div("🏷️", style={'fontSize': '32px', 'marginBottom': '8px'}),
                    html.H4(f"{len(tags_with_data)}", style={
                        'margin': '0',
                        'fontSize': '32px',
                        'fontWeight': '800',
                        'color': LIGHT_THEME['text']
                    }),
                    html.P("Aktywne kategorie", style={
                        'margin': '4px 0 0 0',
                        'fontSize': '14px',
                        'color': LIGHT_THEME['placeholder'],
                        'fontWeight': '500'
                    })
                ], style={
                    'textAlign': 'center',
                    'padding': '20px',
                    'background': 'linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%)',
                    'borderRadius': LIGHT_THEME['radius'],
                    'flex': '1',
                    'margin': '0 10px'
                })
            ], style={'display': 'flex', 'marginBottom': '30px'})
        ]),
        
        # Best and worst performing sections
        html.Div([
            html.Div([
                html.H4("🏆 Najlepiej opanowane", style={
                    'color': LIGHT_THEME['success'],
                    'marginBottom': '16px',
                    'fontWeight': '700',
                    'fontSize': '20px'
                }),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span(f"🎯 {tag}", style={
                                'fontWeight': '600',
                                'fontSize': '16px',
                                'color': LIGHT_THEME['text']
                            }),
                            html.Div([
                                html.Div(style={
                                    'width': f"{tag_stats.get(tag, {'success_rate': 0})['success_rate']*100}%",
                                    'height': '8px',
                                    'background': 'linear-gradient(90deg, #2ecc71 0%, #27ae60 100%)',
                                    'borderRadius': '4px',
                                    'transition': 'width 0.5s ease'
                                }),
                                html.Span(f"{tag_stats.get(tag, {'success_rate': 0})['success_rate']*100:.1f}% ({tag_stats.get(tag, {'solved': 0})['solved']}/{tag_stats.get(tag, {'total': 0})['total']})", style={
                                    'fontSize': '14px',
                                    'color': LIGHT_THEME['success'],
                                    'fontWeight': '600',
                                    'marginLeft': '12px'
                                })
                            ], style={
                                'display': 'flex',
                                'alignItems': 'center',
                                'marginTop': '8px',
                                'background': '#f8f9fa',
                                'padding': '8px',
                                'borderRadius': '6px'
                            })
                        ], style={'marginBottom': '12px'})
                        for tag in best_tags
                    ])
                ]) if best_tags else html.P("Brak danych", style={'color': LIGHT_THEME['placeholder'], 'fontStyle': 'italic'})
            ], style={
                'flex': 1, 
                'padding': '24px',
                'background': 'linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%)',
                'borderRadius': LIGHT_THEME['radius'],
                'marginRight': '15px',
                'border': f"2px solid {LIGHT_THEME['success']}20"
            }),
            html.Div([
                html.H4("⚠️ Wymagają poprawy", style={
                    'color': LIGHT_THEME['error'],
                    'marginBottom': '16px',
                    'fontWeight': '700',
                    'fontSize': '20px'
                }),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span(f"📌 {tag}", style={
                                'fontWeight': '600',
                                'fontSize': '16px',
                                'color': LIGHT_THEME['text']
                            }),
                            html.Div([
                                html.Div(style={
                                    'width': f"{tag_stats.get(tag, {'success_rate': 0})['success_rate']*100}%",
                                    'height': '8px',
                                    'background': 'linear-gradient(90deg, #e74c3c 0%, #c0392b 100%)',
                                    'borderRadius': '4px',
                                    'transition': 'width 0.5s ease'
                                }),
                                html.Span(f"{tag_stats.get(tag, {'success_rate': 0})['success_rate']*100:.1f}% ({tag_stats.get(tag, {'solved': 0})['solved']}/{tag_stats.get(tag, {'total': 0})['total']})", style={
                                    'fontSize': '14px',
                                    'color': LIGHT_THEME['error'],
                                    'fontWeight': '600',
                                    'marginLeft': '12px'
                                })
                            ], style={
                                'display': 'flex',
                                'alignItems': 'center',
                                'marginTop': '8px',
                                'background': '#f8f9fa',
                                'padding': '8px',
                                'borderRadius': '6px'
                            })
                        ], style={'marginBottom': '12px'})
                        for tag in worst_tags
                    ])
                ]) if worst_tags else html.P("Brak danych", style={'color': LIGHT_THEME['placeholder'], 'fontStyle': 'italic'})
            ], style={
                'flex': 1, 
                'padding': '24px',
                'background': 'linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%)',
                'borderRadius': LIGHT_THEME['radius'],
                'marginLeft': '15px',
                'border': f"2px solid {LIGHT_THEME['error']}20"
            })
        ], style={'display': 'flex', 'marginBottom': '30px'}),
        
        # Detailed table
        html.Div([
            html.H4("📋 Szczegółowe statystyki", style={
                'marginBottom': '20px',
                'fontWeight': '700',
                'color': LIGHT_THEME['text'],
                'fontSize': '22px'
            }),
            html.Div([
                html.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("🏷️ Kategoria", style={
                                'textAlign': 'left', 
                                'padding': '16px',
                                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                'color': 'white',
                                'fontWeight': '700',
                                'fontSize': '16px'
                            }),
                            html.Th("📊 Zadania", style={
                                'textAlign': 'center', 
                                'padding': '16px',
                                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                'color': 'white',
                                'fontWeight': '700',
                                'fontSize': '16px'
                            }),
                            html.Th("🎯 Skuteczność", style={
                                'textAlign': 'center', 
                                'padding': '16px',
                                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                'color': 'white',
                                'fontWeight': '700',
                                'fontSize': '16px'
                            }),
                            html.Th("📈 Postęp", style={
                                'textAlign': 'center', 
                                'padding': '16px',
                                'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                'color': 'white',
                                'fontWeight': '700',
                                'fontSize': '16px'
                            })
                        ])
                    ]),
                    html.Tbody([
                        html.Tr([
                            html.Td(tag, style={
                                'padding': '16px', 
                                'borderBottom': '1px solid #eee',
                                'fontWeight': '600',
                                'color': LIGHT_THEME['text']
                            }),
                            html.Td(f"{tag_stats.get(tag, {'solved': 0})['solved']}/{tag_stats.get(tag, {'total': 0})['total']}", style={
                                'textAlign': 'center', 
                                'padding': '16px', 
                                'borderBottom': '1px solid #eee',
                                'fontWeight': '600',
                                'color': LIGHT_THEME['text']
                            }),
                            html.Td([
                                html.Span(f"{tag_stats.get(tag, {'success_rate': 0})['success_rate']*100:.1f}%", style={
                                    'fontWeight': '700',
                                    'color': LIGHT_THEME['success'] if tag_stats.get(tag, {'success_rate': 0})['success_rate'] > 0.6 else LIGHT_THEME['warning'] if tag_stats.get(tag, {'success_rate': 0})['success_rate'] > 0.3 else LIGHT_THEME['error']
                                })
                            ], style={
                                'textAlign': 'center', 
                                'padding': '16px', 
                                'borderBottom': '1px solid #eee'
                            }),
                            html.Td([
                                html.Div([
                                    html.Div(style={
                                        'width': f"{tag_stats.get(tag, {'success_rate': 0})['success_rate']*100}%",
                                        'height': '12px',
                                        'background': f"linear-gradient(90deg, {LIGHT_THEME['success']} 0%, {LIGHT_THEME['success']}cc 100%)" if tag_stats.get(tag, {'success_rate': 0})['success_rate'] > 0.6 else f"linear-gradient(90deg, {LIGHT_THEME['warning']} 0%, {LIGHT_THEME['warning']}cc 100%)" if tag_stats.get(tag, {'success_rate': 0})['success_rate'] > 0.3 else f"linear-gradient(90deg, {LIGHT_THEME['error']} 0%, {LIGHT_THEME['error']}cc 100%)",
                                        'borderRadius': '6px',
                                        'transition': 'width 0.5s ease'
                                    })
                                ], style={
                                    'width': '100%',
                                    'background': '#f1f3f4',
                                    'borderRadius': '6px',
                                    'overflow': 'hidden'
                                })
                            ], style={
                                'textAlign': 'center', 
                                'padding': '16px', 
                                'borderBottom': '1px solid #eee'
                            })
                        ], style={
                            'transition': 'background-color 0.2s ease',
                            'background': 'white'
                        }) for tag in sorted_tags
                    ])
                ], style={
                    'width': '100%', 
                    'borderCollapse': 'collapse',
                    'borderRadius': LIGHT_THEME['radius'],
                    'overflow': 'hidden',
                    'boxShadow': LIGHT_THEME['shadow']
                })
            ], style={
                'background': 'white',
                'borderRadius': LIGHT_THEME['radius'],
                'overflow': 'hidden',
                'boxShadow': LIGHT_THEME['shadow']
            })
        ])
    ], style={
        'background': LIGHT_THEME['content_bg'],
        'padding': '32px',
        'borderRadius': LIGHT_THEME['radius'],
        'boxShadow': LIGHT_THEME['shadow']
    })
    return summary

# Usunięto domyślne kategorie - użytkownicy dodają własne kategorie przez interfejs

def clear_all_categories():
    """Wyczyść wszystkie kategorie z bazy danych"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Najpierw usuń powiązania zadań z kategoriami
    cur.execute("DELETE FROM zadanie_kategoria")
    
    # Następnie usuń wszystkie kategorie
    cur.execute("DELETE FROM kategoria")
    
    conn.commit()
    rows_affected = cur.rowcount
    cur.close()
    conn.close()
    
    return rows_affected

def clear_all_tasks():
    """Wyczyść wszystkie zadania z bazy danych"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Usuń powiązania zadań z kategoriami
    cur.execute("DELETE FROM zadanie_kategoria")
    
    # Usuń wszystkie zadania
    cur.execute("DELETE FROM Zadanie")
    
    # Usuń wszystkie zestawy
    cur.execute("DELETE FROM zestaw_matura")
    
    conn.commit()
    cur.close()
    conn.close()
    
    return True

def clear_entire_database():
    """Wyczyść całą bazę danych"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Usuń wszystko w odpowiedniej kolejności (ze względu na klucze obce)
        cur.execute("DELETE FROM zadanie_kategoria")
        cur.execute("DELETE FROM Zadanie")
        cur.execute("DELETE FROM zestaw_matura")
        cur.execute("DELETE FROM kategoria")
        
        conn.commit()
        result = True
    except Exception as e:
        conn.rollback()
        result = False
    finally:
        cur.close()
        conn.close()
    
    return result

def get_kategoria_by_id(kategoria_id):
    """Pobierz kategorię po ID"""
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM kategoria WHERE id = ?", (kategoria_id,))
    kategoria = cur.fetchone()
    cur.close()
    conn.close()
    return kategoria

def get_kategorie_by_ids(kategorie_ids):
    """Pobierz kategorie po listie ID"""
    if not kategorie_ids:
        return []
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    placeholders = ','.join(['?' for _ in kategorie_ids])
    cur.execute(f"SELECT * FROM kategoria WHERE id IN ({placeholders})", kategorie_ids)
    kategorie = cur.fetchall()
    cur.close()
    conn.close()
    return kategorie

def get_kategorie_for_subject(subject):
    """Pobierz wszystkie kategorie dla danego przedmiotu"""
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM kategoria WHERE subject = ?", (subject,))
    kategorie = cur.fetchall()
    cur.close()
    conn.close()
    return kategorie

def get_kategorie_for_zestaw(zestaw_id):
    """Pobierz wszystkie kategorie dla zestawu (na podstawie przedmiotu zestawu)"""
    # Najpierw pobierz przedmiot zestawu
    zestaw = fetch_zestaw_by_id(zestaw_id)
    if not zestaw:
        return []
    
    # Następnie pobierz kategorie dla tego przedmiotu
    return get_kategorie_for_subject(zestaw['subject'])

def add_new_kategoria(nazwa, subject):
    """Dodaj nową kategorię do bazy danych dla danego przedmiotu"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Sprawdź czy kategoria już istnieje dla tego przedmiotu
    cur.execute(
        "SELECT id FROM kategoria WHERE nazwa = ? AND subject = ?", 
        (nazwa, subject)
    )
    existing = cur.fetchone()
    
    if existing:
        cur.close()
        conn.close()
        return None  # Kategoria już istnieje
    
    # Dodaj nową kategorię (bez zestaw_matura_id)
    cur.execute(
        "INSERT INTO kategoria (nazwa, subject) VALUES (?, ?)",
        (nazwa, subject)
    )
    conn.commit()
    kategoria_id = cur.lastrowid
    cur.close()
    conn.close()
    return kategoria_id

def delete_kategoria(kategoria_id):
    """Usuń kategorię z bazy danych"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Usuń powiązania z zadaniami
    cur.execute("DELETE FROM zadanie_kategoria WHERE kategoria_id = ?", (kategoria_id,))
    
    # Usuń kategorię
    cur.execute("DELETE FROM kategoria WHERE id = ?", (kategoria_id,))
    conn.commit()
    rows_affected = cur.rowcount
    cur.close()
    conn.close()
    return rows_affected > 0
