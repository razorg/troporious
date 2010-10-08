from jinja2 import Environment, FileSystemLoader
import os

template_dirs = [os.path.join(os.path.dirname(__file__), 'templates')]
env = Environment(loader=FileSystemLoader(template_dirs))
APPS_INSTALLED = [
  'apps.validation',
]                                 
