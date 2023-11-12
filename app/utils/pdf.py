import os
import pdfkit
from flask import render_template 
from celery import shared_task


class PDFCreator():
    def __init__(self, template_name, output_filename):
        self.template_name = template_name
        #self.default_path = default_path
        self.output_filename = output_filename
    
    def render_template(self, context):
        """Render Jinja2 template with given context."""
        return render_template(self.template_name, **context)

    def create_pdf(self, html):
        #os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
        pdfkit.from_string(html, self.output_filename)

    @shared_task
    def generate_pdf(self, context):
        html = self.render_template(context)
        self.create_pdf(html)