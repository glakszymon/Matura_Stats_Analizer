import os

def load_html_template(template_name='index_template.html'):
    """
    Load HTML template from templates directory
    """
    template_path = os.path.join('templates', template_name)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Template file {template_path} not found!")
        return None
    except Exception as e:
        print(f"Error loading template: {e}")
        return None