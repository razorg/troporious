"""
if currentCall == None:
  message(
    'your secret is : '+secret, 
    {'network' : 'MSN', 'to' : 'danmylonakis@gmail.com'})
else:
  answer()
  message = currentCall.initialText
  if message == 'OK!':
    say('you said OK!')
  else:
    say('you didnt say the word!')
"""
import urllib2, urllib
global got_it, times
got_it = False
times = 0

def logger(string):
  log("LOGGED : "+string)

def onCorrectResponse(event):
  global got_it
  global times
  answer = event.choice.utterance.replace(' ', '')
  if (answer == secret):
    req_params = {
      'access_key':access_key,
      'result':'done'
    }
    response = urllib2.urlopen('http://smsandvoice.appspot.com/BackendResponse?'+urllib.urlencode(req_params))
    got_it = True
  else:
    times = times + 1
  
def onWrongResponse(event):
  say("Your input was wrong.")
  
def onTimeout(event):
  say("You didn't input something in a long time.")

def say_as(value,type):
    ssml_start="<?xml version='1.0'?><speak>"
    ssml_end="</say-as></speak>"
    ssml ="<say-as interpret-as='vxml:"+ type + "'>" + value+""
    complete_string = ssml_start + ssml + ssml_end
    say(complete_string)

def onAnswer(event):
  global got_it
  global times
  say("Please press or say the following numbers.")
  say_as(secret,'digits')
  while not got_it:
    if (times > 3):
      say("This is your last chance.")
    ask('', {'choices':'[4 DIGITS]','timeout':10.0,'terminator':'#','onChoice':onCorrectResponse})
    if (times > 3) and (not got_it):
      say("You tried 5 times and failed. I'm hanging up!")
      hangup()
      return
    if not got_it:
      say("Wrong! Try again...")
    else:
      say("Correct. You are now validated.")
      hangup()
      return
  assert(False, 'cant go here')

call(to,
  {
    'onAnswer':onAnswer,
    'onBadChoice':onWrongResponse,
    'onTimeout':onTimeout
  })

