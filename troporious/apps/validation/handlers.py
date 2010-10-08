from helpers import TemplatedRequest
from google.appengine.ext import webapp
from apps.validation.models import ValidationRequest, ServiceUser
import re, random, hmac, urllib2, urllib, os, logging, string, datetime
from google.appengine.ext import db
import simplejson as json
import tropo

TROPO_TOKEN_ONLY_SAY = '6651a75d44ece74d87518ce880b9fa550d1a90dcf507f59134cb69f5a5e72fabe52bcb29b32dabf75c900f92'
SECRET_LENGTH = 4
SECRET_CHARS = string.digits

def api_key_exists(api_key):
  return db.GqlQuery('SELECT * FROM ServiceUser WHERE api_key = :1', api_key).count()

class ValidatorDemoHandler(webapp.RequestHandler, TemplatedRequest):
  def get(self):
    step = self.request.get('step')
    if not step:
      step = '1'
    context = dict()
    if step == '2':
      context['step'] = 3
      context['access_key'] = self.request.get('access_key')
    return self.render_response('validation-demo-'+step+'.html', context)
  
  def post(self):
    step = self.request.get('step')
    phone = self.request.get('phone')
    if (not phone) and (not step):
      return self.response.out.write('no phone given')
    
    if (step):
      access_key = self.request.get('access_key')
      secret = self.request.get('secret')
      ds_entry = db.GqlQuery('SELECT * FROM ValidationRequest WHERE access_key = :1',access_key)
      ds_entry = ds_entry.get()
      if (ds_entry.secret == int(secret)):
        return self.render_response('validation-demo-right.html')
      else:
        return self.render_response('validation-demo-wrong.html')
    else:
      target = 'tel:'+phone
      secret = tropo.generate_secret()
      access_key = tropo.generate_key()
      call_context = {
        'to':target,
        'intro':'This is our service demo! Your secret code is :',
        'secret':secret,
        'access_key':access_key
      }
      tropo.tropo_run_script(call_context)
      ds_req = ValidationRequest(
            target = target,
            api_key = tropo.DEMO_API_KEY,
            access_key = access_key,
            secret = int(secret)
            )
      ds_req.put()
    return self.redirect('/validator/demo?step=2&access_key='+access_key)


class BackendResponseHandler(webapp.RequestHandler):
  def get(self):
    access_key = self.request.get('access_key')
    result = self.request.get('result')
    if (not result) or (not access_key):
      return self.response.out.write('no result or access_key')
    
    key_entry = db.GqlQuery('SELECT * FROM ValidationRequest WHERE access_key = :1', access_key)
    if (key_entry.count() == 0):
      return self.response.out.write('no such pending request with such access key')
    assert key_entry.count() == 1, 'duplicate entries! omagad!'
    key_entry_obj = key_entry.get()
    key_entry_obj.result = result
    key_entry_obj.put()
    return self.response.out.write('')

class ValidatorHandler(webapp.RequestHandler, TemplatedRequest):
  def get(self):
    do = self.request.get('do')
    if (do == 'delete_requests'):
      ds_requests = db.GqlQuery("SELECT __key__ FROM ValidationRequest").fetch(200)
      db.delete(ds_requests)
      return self.redirect('/validator')
      
    service_users = ServiceUser.all()
    service_users.count = service_users.count()
    validation_requests = ValidationRequest.all()
    validation_requests.count = validation_requests.count()
    return self.render_response('validator.html', validation_requests=validation_requests, service_users=service_users)
  
  def post(self):
    method = self.request.get("method")
    if (method == "new_service_user"):
      name = self.request.get('name')
      existing = db.GqlQuery("SELECT * FROM ServiceUser WHERE name = :1", name)
      if (existing.count() != 0):
        return self.response.out.write('already exists')
      else:
        new_user = ServiceUser(name=name, api_key=hmac.new(str(random.random())).hexdigest())
        new_user.put()
        return self.redirect('/validator')
    else:
      return self.response.out.write('no type')
  
class ValidateHandler(webapp.RequestHandler):
    def get(self):
      target = self.request.get('target')
      api_key = self.request.get('api_key')
      secret = self.request.get('secret')
      intro = self.request.get('intro')
      if (not target) or (not api_key):
        return self.response.out.write('target and service key is required params.')
                                                                       
      method = re.match('(\\w+):', target)
      if (method is None):
        return self.response.out.write('target '+target+' not valid')
      
      if (not api_key_exists(api_key)):
        return self.response.out.write('api key ' + api_key + ' does not exist')
      
      
      method = method.group(1)
      access_key = hmac.new(str(random.random())).hexdigest()
      if (method == 'tel' or 'sip'):
        if not secret:
          secret = "".join(random.choice(SECRET_CHARS) for x in range(SECRET_LENGTH))
        if not intro:
          intro = "Hello! Your secret code is :"
        tropo_params = {
          'action':'create',
          'token':TROPO_TOKEN_ONLY_SAY,
          'to':target,
          'secret':secret,
          'intro':intro,
          'access_key':access_key
        }
        tropo_request = urllib2.urlopen('http://api.tropo.com/1.0/sessions?'+urllib.urlencode(tropo_params))
        req = ValidationRequest(
          target = target,
          api_key = api_key,
          access_key = access_key,
          secret = int(secret)
          )
        req.put()
        resp = json.dumps({'access_key':access_key,'secret':secret})
        return self.response.out.write(resp)
      return self.response.out.write('method not supported.')
