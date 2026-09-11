import base64
from pathlib import Path

def encode_image(filepath):
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode()

hero = encode_image('a:/ST Failure/assets/hero_bg.jpg')
footer = encode_image('a:/ST Failure/assets/footer_bg.jpg')

css_path = Path('a:/ST Failure/assets/style.css')
css = css_path.read_text(encoding='utf-8')
css = css.replace('url("app/static/hero_bg.jpg")', f'url("data:image/jpeg;base64,{hero}")')

css += f'''
.ag-footer-banner {{
    background-image: url("data:image/jpeg;base64,{footer}");
    background-size: cover;
    background-position: center;
}}
'''
css_path.write_text(css, encoding='utf-8')
print("CSS updated successfully")
