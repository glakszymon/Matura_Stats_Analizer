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

def insert_zadanie(id_zestawu, nr_zadania, nazwa, tresc, solved, tags):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Zadanie (id_zestawu, nr_zadania, nazwa, tresc, solved, tags, created_at)
        VALUES (?, ?, ?, ?, ?, ?, NOW())
        """,
        (id_zestawu, nr_zadania, nazwa, tresc, int(solved), ",".join(tags))
    )
    conn.commit()
    cur.close()
    conn.close()

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
    cur.execute(
        "SELECT * FROM Zadanie WHERE id_zestawu = ? ORDER BY nr_zadania ASC",
        (zestaw_id,)
    )
    zadania = cur.fetchall()
    for zad in zadania:
        zad['tags'] = [t.strip() for t in zad.get('tags', '').split(',')] if zad.get('tags') else []
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
            z.tags as tags,
            z.created_at as created,
            z.id_zestawu as set_id,
            zm.name as set_name
        FROM Zadanie z
        LEFT JOIN zestaw_matura zm ON z.id_zestawu = zm.id
        ORDER BY z.created_at DESC
    """)
    zadania = cur.fetchall()
    for zad in zadania:
        zad['tags'] = [t.strip() for t in zad.get('tags', '').split(',')] if zad.get('tags') else []
        zad['solved'] = bool(zad['solved'])
    cur.close()
    conn.close()
    return zadania

# utils.py
from theme import LIGHT_THEME
import math
from dash import html

TAGS = [
    "#Geometria_Analityczna",
    "#Planimetria",
    "#Stereometria",
    "#Kombinatoryka",
    "#Rachunek_Prawdopodobieństwa",
    "#Funkcje",
    "#Ciągi",
    "#Trygonometria",
    "#Równania_i_Nierówności",
    "#Optymalizacja",
    "#Dowody"
]

def calculate_tag_stats(tasks):
    tag_stats = {}
    for tag in TAGS:
        total = 0
        solved = 0
        for task in tasks:
            if tag in task['tags']:
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

import plotly.graph_objects as go

def create_radar_chart(tag_stats):
    num_tags = len(TAGS)
    values = [tag_stats[tag]['success_rate'] for tag in TAGS]
    values += values[:1]
    r = [1] * (num_tags + 1)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r,
        theta=[tag.replace('_', ' ') for tag in TAGS] + [TAGS[0].replace('_', ' ')],
        fill='toself',
        fillcolor='rgba(80,112,255,0.08)',
        line=dict(color='rgba(80,112,255,0.15)'),
        name='Zakres',
        hoverinfo='none'
    ))
    for i, tag in enumerate(TAGS):
        fig.add_trace(go.Scatterpolar(
            r=[values[i]],
            theta=[tag.replace('_', ' ')],
            mode='markers',
            marker=dict(
                size=18,
                color='#38b6ff' if values[i] > 0.5 else '#e74c3c',
                opacity=0.9,
                line=dict(width=2, color='#fff')
            ),
            name=tag.replace('_', ' '),
            text=f"{tag.replace('_', ' ')}<br>Rozwiązane: {tag_stats[tag]['solved']}/{tag_stats[tag]['total']}<br>Skuteczność: {tag_stats[tag]['success_rate']*100:.1f}%",
            hoverinfo='text'
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], showticklabels=False, ticks=''),
            angularaxis=dict(rotation=90, direction='clockwise')
        ),
        showlegend=False,
        title='Poziom opanowania materiału',
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_stats_summary(tag_stats):
    sorted_tags = sorted(TAGS, key=lambda x: tag_stats[x]['success_rate'], reverse=True)
    summary = html.Div([
        html.H3("Podsumowanie", style={'marginBottom': '18px', 'fontWeight': 'bold'}),
        html.Div([
            html.Div([
                html.H4("Najlepiej opanowane", style={'color': LIGHT_THEME['success']}),
                html.Ul([
                    html.Li(f"{tag.replace('_', ' ')}: {tag_stats[tag]['success_rate']*100:.1f}% ({tag_stats[tag]['solved']}/{tag_stats[tag]['total']})")
                    for tag in sorted_tags[:3] if tag_stats[tag]['total'] > 0
                ])
            ], style={'flex': 1, 'padding': '10px'}),
            html.Div([
                html.H4("Najsłabiej opanowane", style={'color': LIGHT_THEME['error']}),
                html.Ul([
                    html.Li(f"{tag.replace('_', ' ')}: {tag_stats[tag]['success_rate']*100:.1f}% ({tagStats[tag]['solved']}/{tagStats[tag]['total']})")
                    for tag in sorted_tags[-3:] if tag_stats[tag]['total'] > 0
                ])
            ], style={'flex': 1, 'padding': '10px'})
        ], style={'display': 'flex', 'marginBottom': '18px'}),
        html.Div([
            html.H4("Wszystkie tagi", style={'marginBottom': '10px'}),
            html.Table(
                [html.Tr([
                    html.Th("Temat", style={'textAlign': 'left', 'padding': '8px'}),
                    html.Th("Zadania", style={'textAlign': 'center', 'padding': '8px'}),
                    html.Th("Skuteczność", style={'textAlign': 'right', 'padding': '8px'})
                ])] +
                [html.Tr([
                    html.Td(tag.replace('_', ' '), style={'padding': '8px', 'borderBottom': '1px solid #eee'}),
                    html.Td(f"{tag_stats[tag]['solved']}/{tag_stats[tag]['total']}", style={'textAlign': 'center', 'padding': '8px', 'borderBottom': '1px solid #eee'}),
                    html.Td([
                        html.Div(
                            style={
                                'width': f"{tag_stats[tag]['success_rate']*100}%",
                                'height': '18px',
                                'background': LIGHT_THEME['success'] if tag_stats[tag]['success_rate'] > 0.5 else LIGHT_THEME['warning'],
                                'borderRadius': '4px',
                                'transition': 'width 0.4s'
                            }
                        ),
                        html.Span(f"{tag_stats[tag]['success_rate']*100:.1f}%", style={'marginLeft': '10px'})
                    ], style={'textAlign': 'right', 'padding': '8px', 'borderBottom': '1px solid #eee', 'display': 'flex', 'alignItems': 'center'})
                ]) for tag in sorted_tags if tag_stats[tag]['total'] > 0],
                style={'width': '100%', 'borderCollapse': 'collapse'}
            )
        ])
    ])
    return summary
    return summary
    return summary
    return summary
