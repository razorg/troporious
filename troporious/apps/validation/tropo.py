import urllib
import hmac, random, string
from google.appengine.api import urlfetch


SCRIPT_RUN_URL='http://api.tropo.com/1.0/sessions?'
SECRET_CHARS = string.digits
SECRET_LENGTH = 4
API_KEY_INFINITE = 'ICHEAT'
TROPO_TOKEN_ONLY_SAY = '69508eb2bd3f2e44a548758c68b48ae03c6d8b3cd0da5524387e9ee871f8dd5b56bf474ef80360fbf47ce1f7'
DEMO_API_KEY = 'KEYISDEMO'




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

