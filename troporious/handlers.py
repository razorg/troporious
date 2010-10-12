from helpers import TemplatedRequest
from google.appengine.ext import webapp

class RootHandler(webapp.RequestHandler, TemplatedRequest):
    def get(self):
      #self.response.headers['Cache-Control'] = ("no-cache, no-store, must-revalidate, max-age=-1") 
      #self.response.headers['Content-Encoding'] = "none"
      return self.render_response('root.html')
