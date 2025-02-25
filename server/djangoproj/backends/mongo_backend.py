# myapp/backends/custom_backend.py

from django.template.backends.base import BaseEngine
from django.template import Template
from django.template.backends.django import DjangoTemplates
from django.template.loader import get_template

class Mongo_Backend(BaseEngine):
    def __init__(self, params):
        super().__init__(params)
        self.django_backend = DjangoTemplates(params)

    def from_string(self, template_code):
        return self.django_backend.from_string(template_code)

    def get_template(self, template_name):
        try:
            template = get_template(template_name)
            return template
        except Exception as e:
            print(f"Error loading template: {e}")
            raise

    def render_template(self, template_name, context):
        template = self.get_template(template_name)
        return template.render(context)
