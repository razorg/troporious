import urllib2, urllib,sys, threading, time


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
  urllib2.urlopen('%s/validator/BackendResponse?%s' % (callback_host, urllib.urlencode(req_params)))


def onAnswer(event):
    #if self_recorded == "on":
    #    logger("i play recorded file...")
    #    say("http://hosting.tropo.com/49422/www/audio/geia sas.wav")
    #else:
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
class FuckedUpChecker(threading.Thread):
  def run(self):
    time.sleep(3)
    logger('FROM THREAD : fucker = %s' % fucked_up)
    if (fucked_up == False): 
      notify_back('called')

fut = FuckedUpChecker()
fut.run()
try:
  call(to,
    {
    'answerOnMedia':True,
    'onAnswer':onAnswer,
    'onCallFailure':onCallFailure,
    'onTimeout':onTimeout,
    'onError':onError,
    #'recordFormat':'audio/mp3',
    #'recordURI':'http://smsandvoice.appspot.com/validator/BackendRecord'
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

