from google.appengine.ext import webapp
from google.appengine.api import urlfetch

class ProxyHandler(webapp.RequestHandler):
    def get(self):
        url = self.request.get('url')
        if not url:
            return self.response.out.write('no url specified')
        return self.response.out.write(urlfetch.fetch(url).content)
        
