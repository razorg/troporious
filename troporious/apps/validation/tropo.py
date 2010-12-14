import urllib
import hmac, random, string
from google.appengine.api import urlfetch


SCRIPT_RUN_URL='http://api.tropo.com/1.0/sessions?'
TROPO_TOKEN_ONLY_SAY = 'ea7e10c4438c5146ac1fba85fe4c22316a76aa21b03b4839f7a03b690c7d7d83169db5964fa2482aff3a2f6d'

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

