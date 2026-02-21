import json
import os
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

from Certificate import Certificate

class SocialFoundationCertificate(Certificate):

    def render():
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('SocialFoundationCertificate.html') 
        data['logo_path'] = 'logo.png' 

        html_content = template.render(**data)

        tmp_path = os.path.join('templates', 'tmp.html')
        with open(tmp_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--allow-file-access-from-files'])
            page = browser.new_page(viewport={'width':900, 'height': 800})
            page.goto(f"file://{os.path.abspath(tmp_path)}", wait_until="networkidle")
            page.wait_for_function('document.fonts.ready')
            page.screenshot(path="output.png")
            browser.close()

        os.remove(tmp_path)
        print("Done")