from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
import re
from models.SMSAttempt import SMSAttempt
import datetime
import logging
from google.appengine.ext import db
import datetime

class MainPage(webapp.RequestHandler):
    def get(self):
        templ_vars = { }
        path = os.path.dirname(__file__)
        if (self.request.get("attempt") == "success"):
            self.response.out.write(template.render(path+'/html/success.html', templ_vars))
        else:
            self.response.out.write(template.render(path+'/html/form.html', templ_vars))
    
    def post(self):
    	templ_vars = {'msg_len_long':True,'to_notvalid':True }
        to = self.request.get("to");
        msg = self.request.get("msg");
        if ((to is not None) and (msg is not None)):
            pattern = re.compile("^\+\d{12}$")
            if (pattern.match(to)):
                templ_vars['to_notvalid'] = False
            if (len(msg) <= 160):
                templ_vars['msg_len_long'] = False
            if ((templ_vars['msg_len_long'] is False) and (templ_vars['to_notvalid'] is False)):
                new_attempt = SMSAttempt(to = to, sent_date = datetime.datetime.now().date())
                new_attempt.put()
                self.redirect("/testform?attempt=success")
            else:
                path = os.path.join(os.path.dirname(__file__), 'html/form.html')
                self.response.out.write(template.render(path, templ_vars))
        else:
       	    self.response.out.write("not valid post data")
    

application = webapp.WSGIApplication([('/testform', MainPage)],debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
