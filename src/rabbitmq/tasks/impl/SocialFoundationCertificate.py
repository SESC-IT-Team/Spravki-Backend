from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from src.rabbitmq.tasks.AbstractCertificate import AbstractCertificate
from src.rabbitmq.tasks.impl.SocialFoundationCertificateSchema import SocialFoundationCertificateSchema


class SocialFoundationCertificate(AbstractCertificate):
    @staticmethod
    def render(data: SocialFoundationCertificateSchema):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('SocialFoundationCertificate.html') 
        data['logo_path'] = 'logo.png' 

        html_content = template.render(**data.model_dump())

        base_dir = Path(__file__).resolve().parent
        template_dir = base_dir / 'src' / 'templates'

        base_url_uri = template_dir.as_uri()

        html_doc = HTML(string=html_content, base_url=base_url_uri)

        output_filename = base_dir / 'certificate.pdf'
        html_doc.write_pdf(str(output_filename))
