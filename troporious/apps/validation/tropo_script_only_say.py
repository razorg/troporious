import urllib2, urllib,sys

def logger(string):
  log("LOGGED : "+string)

def say_as(value,type):
    ssml_start="<?xml version='1.0'?><speak>"
    ssml_end="</say-as></speak>"
    ssml ="<say-as interpret-as='vxml:"+ type + "'>" + value+""
    complete_string = ssml_start + ssml + ssml_end
    say(complete_string)


def notify_back(result):
  logger('NOTIFYING : %s' % result)
  req_params = {
    'result':result,
    'access_key':access_key
  }
  urllib2.urlopen('http://smsandvoice.appspot.com/validator/BackendResponse?'+urllib.urlencode(req_params))


def onAnswer(event):
  say(intro)
  say_as(secret,'digits')
  say("i repeat.")
  say_as(secret,'digits')
  hangup()
  notify_back('done')

def onCallFailure():
  notify_back('call_failure')

def onTimeout():
  notify_back('timeout')
  
def onError():
  notify_back('call_failed')

fucked_up = False

try:
  call(to,
    {
    'answerOnMedia':True,
    'onAnswer':onAnswer,
    'onCallFailure':onCallFailure,
    'onTimeout':onTimeout,
    'onError':onError
    })
except:
  inst = sys.exc_info()
  logger("Unexpected error: "+str(inst[0]) + ' ' + str(inst[1]) + ' ' + str(inst[2]))
  fucked_up = True
  
logger('fucked up = %s' % str(fucked_up))
if fucked_up == False:
  notify_back('called')
#else:
#  notify_back('call failed')

