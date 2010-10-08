from tipfy import RequestHandler, Response, abort
from tipfy.ext.jinja2 import render_response


class RootHandler(RequestHandler):
    def get(self, **kwargs):
        return render_response('conference.html', message={})
