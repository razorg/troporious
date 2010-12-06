from helpers import TemplatedRequest
from google.appengine.ext import webapp

class RootHandler(webapp.RequestHandler, TemplatedRequest):
    def get(self):
      return self.redirect("/playground")
