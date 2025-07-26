# theme.py
LIGHT_THEME = {
    'background': 'linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%)',
    'sidebar_bg': 'linear-gradient(135deg, #232526 0%, #414345 100%)',
    'content_bg': '#ffffffcc',
    'text': '#22223b',
    'text_light': '#ffffff',
    'input_bg': '#f4f6fb',
    'button_primary': 'linear-gradient(90deg, #4f8cff 0%, #38b6ff 100%)',
    'button_danger': '#e74c3c',
    'button_success': '#2ecc71',
    'border': '#e0e0e0',
    'checkbox': '#38b6ff',
    'placeholder': '#bfc9d1',
    'error': '#e74c3c',
    'hover': '#e3e8f0',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'shadow': '0 4px 24px rgba(80, 112, 255, 0.10)',
    'shadow_strong': '0 8px 32px rgba(80, 112, 255, 0.20)',
    'radius': '12px',
    'radius_large': '16px',
    'font': 'Inter, Segoe UI, Arial, sans-serif',
    
    # Enhanced purple theme colors
    'gradient_primary': 'linear-gradient(90deg, #4f8cff 0%, #38b6ff 100%)',
    'gradient_secondary': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'gradient_warning': 'linear-gradient(90deg, #ffecd2 0%, #fcb69f 100%)',
    'gradient_info': 'linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)',
    
    # Glass effect colors
    'glass_bg': 'rgba(255, 255, 255, 0.1)',
    'glass_border': 'rgba(255, 255, 255, 0.2)',
    'glass_shadow': '0 8px 32px rgba(31, 38, 135, 0.37)',
    
    # Status colors
    'status_solved': '#10b981',
    'status_unsolved': '#ef4444',
    'status_partial': '#ed8936',
    
    # Chart colors
    'chart_colors': [
        '#667eea', '#764ba2', '#f093fb', '#f5576c', '#a8edea',
        '#fed6e3', '#d299c2', '#fef9d7', '#48bb78', '#ed8936', '#e53e3e'
    ]
}

DARK_THEME = {
    'background': 'linear-gradient(135deg, #1a1a1a 0%, #2d2d30 100%)',
    'sidebar_bg': 'linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%)',
    'content_bg': '#1e1e1e99',
    'text': '#e0e0e0',
    'text_light': '#ffffff',
    'input_bg': '#2d2d30',
    'button_primary': 'linear-gradient(90deg, #4f8cff 0%, #38b6ff 100%)',
    'button_danger': '#e74c3c',
    'button_success': '#2ecc71',
    'border': '#404040',
    'checkbox': '#38b6ff',
    'placeholder': '#888888',
    'error': '#e74c3c',
    'hover': '#3a3a3a',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'shadow': '0 4px 24px rgba(0, 0, 0, 0.4)',
    'shadow_strong': '0 8px 32px rgba(0, 0, 0, 0.6)',
    'radius': '12px',
    'radius_large': '16px',
    'font': 'Inter, Segoe UI, Arial, sans-serif',
    
    # Enhanced purple theme colors
    'gradient_primary': 'linear-gradient(90deg, #4f8cff 0%, #38b6ff 100%)',
    'gradient_secondary': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'gradient_warning': 'linear-gradient(90deg, #ffecd2 0%, #fcb69f 100%)',
    'gradient_info': 'linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)',
    
    # Glass effect colors
    'glass_bg': 'rgba(255, 255, 255, 0.05)',
    'glass_border': 'rgba(255, 255, 255, 0.1)',
    'glass_shadow': '0 8px 32px rgba(0, 0, 0, 0.5)',
    
    # Status colors
    'status_solved': '#10b981',
    'status_unsolved': '#ef4444',
    'status_partial': '#ed8936',
    
    # Chart colors
    'chart_colors': [
        '#667eea', '#764ba2', '#f093fb', '#f5576c', '#a8edea',
        '#fed6e3', '#d299c2', '#fef9d7', '#48bb78', '#ed8936', '#e53e3e'
    ]
}

# Global theme store - defaults to light
CURRENT_THEME = LIGHT_THEME

def get_theme(theme_name='light'):
    """Get theme colors based on theme name"""
    if theme_name == 'dark':
        return DARK_THEME
    return LIGHT_THEME
