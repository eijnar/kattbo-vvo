import os
import pdfkit
from flask import render_template
from celery import shared_task


class PDFCreator():
    def __init__(self, template_name, output_filename):
        self.template_name = template_name
        self.output_filename = output_filename

    def get_pdf_options(self):
        return {
            'encoding': 'UTF-8',
            'page-size': 'A4',
            'encoding': 'utf-8',
            'margin-top': '25mm',
            'margin-bottom': '25mm',
            'margin-left': '25mm',
            'margin-right': '25mm'
        }

    def render_template(self, context):
        """Render Jinja2 template with given context."""
        return render_template(self.template_name, **context)

    def create_pdf(self, html):
        pdfkit.from_string(html, self.output_filename,
                           options=self.get_options())

    def generate_pdf(self, context):
        html = self.render_template(context)
        print(html)
        self.create_pdf(html)
