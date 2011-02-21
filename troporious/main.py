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
from apps.validation.handlers import PlaygroundHandler, \
                                     PlaygroundLiveHandler

from apps.proxy.handlers import ProxyHandler

from jinja2 import Environment, FileSystemLoader

rules = [
  ('/',PlaygroundHandler),
  ('/StartSession', PlaygroundLiveHandler),
  ('/PlaygroundBackend', PlaygroundLiveHandler)
]
app = webapp.WSGIApplication(rules, debug=True)

def main():
    run_wsgi_app(app)


if __name__ == '__main__':
    main()
