import urllib
import hmac, random, string
from google.appengine.api import urlfetch


SCRIPT_RUN_URL='http://api.tropo.com/1.0/sessions?'
SECRET_CHARS = string.digits
SECRET_LENGTH = 4
TROPO_TOKEN_ONLY_SAY = '79defb2f1373094f9b8ab8e4120df4b3c816f029095abb16affb9f36ab1f3a5983ba77f5c242f31489ae6e87'




def tropo_run_script(context, async=False, callback=None):
  if 'action' not in context.keys():
    context['action'] = 'create'
  if 'token' not in context.keys():
    context['token'] = TROPO_TOKEN_ONLY_SAY
  if (async):
    rpc = urlfetch.create_rpc(callback=callback)
    urlfetch.make_fetch_call(rpc, SCRIPT_RUN_URL+urllib.urlencode(context))
    return rpc
  return urlfetch.fetch(SCRIPT_RUN_URL+urllib.urlencode(context))
  
def generate_key():
  return hmac.new(str(random.random())).hexdigest()

def generate_secret():
  return "".join(random.choice(SECRET_CHARS) for x in range(SECRET_LENGTH))

