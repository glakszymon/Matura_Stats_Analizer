import dash
from dash import dcc, html, Input, Output, State, ALL
from theme import LIGHT_THEME
from layouts import get_sidebar, get_home_layout, get_stats_layout, get_stats_layout_it
from callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Custom CSS for enhanced responsive styling
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
            
            /* Responsive base styles */
            .container {
                width: 100%;
                padding-right: 15px;
                padding-left: 15px;
                margin-right: auto;
                margin-left: auto;
            }
            
            @media (min-width: 576px) {
                .container {
                    max-width: 540px;
                }
            }
            
            @media (min-width: 768px) {
                .container {
                    max-width: 720px;
                }
            }
            
            @media (min-width: 992px) {
                .container {
                    max-width: 960px;
                }
            }
            
            @media (min-width: 1200px) {
                .container {
                    max-width: 1140px;
                }
            }
            
            /* Mobile menu button */
            .mobile-menu-btn {
                display: none;
                background: rgba(255,255,255,0.2);
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                color: white;
                font-size: 24px;
                cursor: pointer;
                backdrop-filter: blur(5px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                position: fixed;
                top: 15px;
                left: 15px;
                z-index: 1002; /* Wyższy niż sidebar */
                transition: all 0.3s ease;
            }
            
            .mobile-menu-btn:hover {
                background: rgba(255,255,255,0.3);
                transform: scale(1.1);
            }
            
            /* Sidebar responsiveness */
            .sidebar {
                position: fixed;
                top: 0;
                left: 0;
                bottom: 0;
                width: 280px;
                transition: transform 0.3s ease;
                z-index: 1001; /* Wyższy niż overlay */
            }
            
            .sidebar.collapsed {
                transform: translateX(-280px);
            }
            
            .page-content.expanded {
                margin-left: 0;
            }
            
            @media (max-width: 992px) {
                .sidebar {
                    width: 240px !important;
                    transform: translateX(-100%);
                    transition: transform 0.3s ease;
                    z-index: 1001 !important;
                    position: fixed !important;
                }
                
                .sidebar.open {
                    transform: translateX(0);
                }
                
                .page-content {
                    margin-left: 0 !important;
                    padding-left: 15px;
                    padding-right: 15px;
                }
                
                .mobile-menu-btn {
                    display: block !important;
                }
            }
            
            @media (min-width: 993px) {
                .mobile-close-btn {
                    display: flex !important;
                }
            }
            
            /* Responsive cards */
            .card-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }
            
            .card {
                flex: 1 1 300px;
                min-width: 0;
            }
            
            /* Responsive tables */
            .responsive-table {
                width: 100%;
                overflow-x: auto;
            }
            
            /* Mobile optimizations */
            @media (max-width: 768px) {
                h1 {
                    font-size: 32px !important;
                }
                
                .feature-cards {
                    flex-direction: column;
                }
                
                .side-panel {
                    width: 100% !important;
                }
                
                .modal-content {
                    padding: 20px 0 !important;
                }
                
                .fab-button {
                    bottom: 20px !important;
                    right: 20px !important;
                    width: 60px !important;
                    height: 60px !important;
                }
                
                .task-card {
                    margin-bottom: 15px;
                }
                
                .stats-grid {
                    grid-template-columns: 1fr !important;
                    gap: 15px !important;
                }
            }
            
            @media (max-width: 480px) {
                .container {
                    padding-left: 10px;
                    padding-right: 10px;
                }
                
                .modal-content > div {
                    padding: 20px !important;
                }
                
                .side-panel .panel-content {
                    padding: 16px !important;
                }
            }
            
            /* Existing hover effects */
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
            
            .add-task-btn:hover {
                background: rgba(255,255,255,0.3) !important;
                transform: translateY(-2px);
            }

            .edit-set-btn:hover {
                background: rgba(255,255,255,0.3) !important;
                transform: translateY(-2px);
            }

            .set-menu-button:hover {
                background: rgba(255,255,255,0.4) !important;
                transform: scale(1.1);
            }

            .dropdown-menu-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
            }

            .set-dropdown-menu {
                position: absolute !important;
                z-index: 9999 !important;
                background: white !important;
                box-shadow: 0 8px 32px rgba(0,0,0,0.15) !important;
            }

            /* Upewnij się, że container ma relative positioning */
            .set-menu-container {
                position: relative !important;
                z-index: 1 !important;
            }
        </style>
    </head>
    <body>
        <!-- Mobile menu button -->
        <button class="mobile-menu-btn" id="mobile-menu-toggle">☰</button>
        
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script>
            // Funkcja do zamykania sidebara
            function closeSidebar() {
                const sidebar = document.querySelector('.sidebar');
                const overlay = document.getElementById('mobile-menu-overlay');
                const pageContent = document.querySelector('.page-content');
                
                if (window.innerWidth <= 992) {
                    sidebar.classList.remove('open');
                    overlay.style.display = 'none';
                } else {
                    sidebar.classList.add('collapsed');
                    pageContent.classList.add('expanded');
                }
            }
            
            // Funkcja do otwierania sidebara
            function openSidebar() {
                const sidebar = document.querySelector('.sidebar');
                const overlay = document.getElementById('mobile-menu-overlay');
                const pageContent = document.querySelector('.page-content');
                
                if (window.innerWidth <= 992) {
                    sidebar.classList.add('open');
                    overlay.style.display = 'block';
                } else {
                    sidebar.classList.remove('collapsed');
                    pageContent.classList.remove('expanded');
                }
            }
            
            // Toggle mobile sidebar
            document.getElementById('mobile-menu-toggle').addEventListener('click', function(e) {
                e.stopPropagation();
                const sidebar = document.querySelector('.sidebar');
                
                if (window.innerWidth <= 992) {
                    if (sidebar.classList.contains('open')) {
                        closeSidebar();
                    } else {
                        openSidebar();
                    }
                } else {
                    if (sidebar.classList.contains('collapsed')) {
                        openSidebar();
                    } else {
                        closeSidebar();
                    }
                }
            });
            
            // Close sidebar when clicking on overlay
            document.addEventListener('click', function(event) {
                const sidebar = document.querySelector('.sidebar');
                const overlay = document.getElementById('mobile-menu-overlay');
                
                if (window.innerWidth <= 992 && 
                    event.target === overlay && 
                    sidebar.classList.contains('open')) {
                    closeSidebar();
                }
            });
            
            // Event listener dla overlay
            document.addEventListener('DOMContentLoaded', function() {
                const overlay = document.getElementById('mobile-menu-overlay');
                if (overlay) {
                    overlay.addEventListener('click', function(e) {
                        if (e.target === overlay) {
                            closeSidebar();
                        }
                    });
                }
            });
            
            // Handle window resize
            window.addEventListener('resize', function() {
                const sidebar = document.querySelector('.sidebar');
                const pageContent = document.querySelector('.page-content');
                const overlay = document.getElementById('mobile-menu-overlay');
                
                if (window.innerWidth > 992) {
                    sidebar.classList.remove('open');
                    overlay.style.display = 'none';
                } else {
                    sidebar.classList.remove('collapsed');
                    pageContent.classList.remove('expanded');
                }
            });
            
            // Close dropdown menus when clicking outside
            document.addEventListener('click', function(event) {
                const menus = document.querySelectorAll('[id*="set-dropdown-menu"]');
                const buttons = document.querySelectorAll('[id*="toggle-set-menu"]');
                
                let clickedButton = false;
                buttons.forEach(button => {
                    if (button.contains(event.target)) {
                        clickedButton = true;
                    }
                });
                
                if (!clickedButton) {
                    menus.forEach(menu => {
                        if (!menu.contains(event.target)) {
                            menu.style.display = 'none';
                        }
                    });
                }
            });
        </script>
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
                            {'label': '📊 Matematyka', 'value': 'matematyka'},
                            {'label': '💻 Informatyka', 'value': 'informatyka'}
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
])

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
