def load_css(css_file):
    with open(css_file, 'r') as f:
        return f'<style>{f.read()}</style>'
