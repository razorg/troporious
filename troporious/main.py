import os
import sys

if 'lib' not in sys.path:
    # Add /lib as primary libraries directory, with fallback to /distlib
    # and optionally to distlib loaded using zipimport.
    sys.path[0:0] = ['lib', 'distlib', 'distlib.zip']

import config
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import handlers
from apps.validation.handlers import ValidatorDemoHandler, \
                                      BackendResponseHandler, \
                                      ValidatorHandler, \
                                      ValidateHandler \

from jinja2 import Environment, FileSystemLoader

rules = [
  ('/',handlers.RootHandler),
  ('/validator/BackendResponse',BackendResponseHandler),
  ('/validator',ValidatorHandler),
  ('/validate',ValidateHandler),
  ('/validator/demo',ValidatorDemoHandler),
]
app = webapp.WSGIApplication(rules, debug=True)

def main():
    run_wsgi_app(app)


if __name__ == '__main__':
    main()
