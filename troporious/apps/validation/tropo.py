import urllib, urllib2
import hmac, random, string

SCRIPT_RUN_URL='http://api.tropo.com/1.0/sessions?'
SECRET_CHARS = string.digits
SECRET_LENGTH = 4
API_KEY_INFINITE = 'ICHEAT'
TROPO_TOKEN_ONLY_SAY = '6651a75d44ece74d87518ce880b9fa550d1a90dcf507f59134cb69f5a5e72fabe52bcb29b32dabf75c900f92'
DEMO_API_KEY = 'KEYISDEMO'

def tropo_run_script(context):
  context['action'] = 'create'
  context['token'] = TROPO_TOKEN_ONLY_SAY
  return urllib2.urlopen(SCRIPT_RUN_URL+urllib.urlencode(context))
  
def generate_key():
  return hmac.new(str(random.random())).hexdigest()

def generate_secret():
  return "".join(random.choice(SECRET_CHARS) for x in range(SECRET_LENGTH))
  
