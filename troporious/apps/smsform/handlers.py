from tipfy import RequestHandler, Response
from tipfy.ext.jinja2 import render_response

class TestFormHandler(RequestHandler):
    def get(self, **kwargs):
        return render_response('form.html', message={})
