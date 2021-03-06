from helpers import TemplatedRequest
from google.appengine.ext import webapp, db
from google.appengine.api import memcache
from apps.validation.models import ValidationRequest, ServiceUser, DemoClient
from django.utils import simplejson as json
import re, urllib, os, logging, time
import tropo

CALLBACK_HOST='http://razorg.webhop.net'

class ValidatorDemoHandler(webapp.RequestHandler, TemplatedRequest):
  def get(self):
    step = self.request.get('step')
    if not step:
      step = '1'
    
    if step == 'fail':
      return self.render_response('validation-demo-fail.html')
        
    context = dict()
    if step == '2':
      context['step'] = 3
      context['access_key'] = self.request.get('access_key')
    return self.render_response('validation-demo-'+step+'.html', context)
  
  def post(self):
    step = self.request.get('step',"")
    phone = self.request.get('phone',"")
    self_recorded = self.request.get('self_recorded',"")
    if (not phone) and (not step):
      return self.response.out.write('no phone given')
    
    if (step):
      access_key = self.request.get('access_key')
      secret = self.request.get('secret')
      ds_entry = ValidationRequest.get_by_key_name(access_key)
      if (ds_entry.secret == int(secret)):
        return self.render_response('validation-demo-right.html')
      else:
        return self.render_response('validation-demo-wrong.html')
    else:
      ip = self.request.remote_addr
      ds_existing = DemoClient.get_by_key_name(ip)
      if not ds_existing:
        DemoClient(key_name=ip, times=1).put(rpc=db.create_rpc())
      else:
        if (ds_existing.times > 4):
          return self.redirect('/validator/demo?step=fail')
        ds_existing.times = ds_existing.times + 1
        ds_existing.put(rpc=db.create_rpc())
      target = 'tel:'+phone
      secret = tropo.generate_secret()
      access_key = tropo.generate_key()
      call_context = {
        'to':target,
        'intro':'This is our service demo! Your secret code is :',
        'secret':secret,
        'access_key':access_key,
        'self_recorded':self_recorded,
        'callback_host':CALLBACK_HOST
      }
      fetch_rpc = tropo.tropo_run_script(call_context, async=True)
      rpc = db.create_rpc()
      validation_entry = ValidationRequest(
            key_name = access_key,
            target = target,
            api_key = tropo.DEMO_API_KEY,
            secret = int(secret)).put(rpc=rpc)
      rpc.wait()
      fetch_rpc.wait()
      
    return self.redirect('/validator/demo?step=2&access_key='+access_key)


class BackendResponseHandler(webapp.RequestHandler):
  def get(self):
    access_key = self.request.get('access_key')
    result = self.request.get('result')
    if (not result) or (not access_key):
      logging.critical('tropo didnt provide access_key or result %s, %s' % (access_key, result))
      return self.response.out.write('no result or access_key')

    key_entry = ValidationRequest.get_by_key_name(access_key)
    if not key_entry:
      logging.critical('tropo requested with access_key %s but it does not exist' % access_key)
    key_entry.result = result
    key_entry.put()
    return self.response.out.write('')

class ValidatorHandler(webapp.RequestHandler, TemplatedRequest):
  def get(self):
    import time
    t2 = time.time()
    do = self.request.get('do')
    if (do == 'delete_requests'):
      db.delete(ValidationRequest.all(keys_only=True).fetch(200))
      return self.redirect('/validator')
    
    elif do == 'delete_quotas':
      db.delete(DemoClient.all(keys_only=True).fetch(200))
      return self.redirect('/validator')
    
    service_users = ServiceUser.all().fetch(100)
    validation_requests = ValidationRequest.all().fetch(100)
    t = time.time()
    for service_user in service_users:
      service_user.api_key = service_user.key().name()
    
    for validation_request in validation_requests:
      validation_request.access_key = validation_request.key().name()  
    now = time.time()
    logging.debug('LOG1%f' %(now - t))
    logging.debug('LOG2%f' %(now - t2))
    context = {
      'service_users':service_users,
      'validation_requests':validation_requests,
    }
    return self.render_response('validator.html', context)
  
  def post(self):
    method = self.request.get("method")
    if (method == "new_service_user"):
      name = self.request.get('name')
      existing = ServiceUser.all(keys_only=True).filter('name = ',name).get()
      if (existing is not None):
        return self.response.out.write('already exists')
      else:
        ServiceUser(name=name, key_name=tropo.generate_key()).put()
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
      
      ds_user_entry = ServiceUser.get_by_key_name(api_key)
      if (not ds_user_entry):
        return self.response.out.write('api key ' + api_key + ' does not exist')
      
      
      method = method.group(1)
      access_key = tropo.generate_key()
      if (method == 'tel' or 'sip'):
        if not secret:
          secret = tropo.generate_secret() 
        if not intro:
          intro = "Hello! Your secret code is :"
        context = {
          'to':target,
          'secret':secret,
          'intro':intro,
          'access_key':access_key
        }
        http_rpc = tropo.tropo_run_script(context, async=True)
        ds_rpc = db.create_rpc()
        ValidationRequest(
          target = target,
          api_key = api_key,
          key_name = access_key,
          secret = int(secret)
        ).put(rpc=ds_rpc)
        resp = json.dumps({'access_key':access_key,'secret':secret})
        http_rpc.wait()
        ds_rpc.wait()
        return self.response.out.write(resp)
      return self.response.out.write('method not supported.')
