import urllib, urllib2, time, sys,os

SERVER = 'http://3.latest.smsandvoice.appspot.com/playground-live'

def logger(string):
    log('LOGGED : %s' % string)

def send_message(context):
    response = None
    try:
        response = urllib2.urlopen(SERVER, urllib.urlencode(context))
    except:
        pass
    else:
        return response.read()
    return None

def do_next_command():
    response = urllib2.urlopen(SERVER, urllib.urlencode({'action':'get_next','session_id':session_id,'from':'tropo'}))
    response = urllib.unquote(response.read())
    logger(response)
    if response == 'wait':
        logger('WAITING')
        return response
    #response = response.split(',')
    #response_dict = dict()
    #for item in response:
    #     items = item.split(':')
    #     response_dict[items[0]] = items[1]
    #logger(str(response) + '     ' +str(response_dict))
    #if response_dict['method'] == 'call':
    #    call('tel:%s' % response_dict['num'])
    #else:
    #    logger('UNKNOWN METHOD "%s"' % response_dict['method'])
    exec(response)

def onAnswer(e):
    say('hello, im your servant.')
    last_non_wait = time.time()
    while last_non_wait + 30 > time.time():
        response = None
        try:
            response = do_next_command()
        except:
            type, value = sys.exc_info()[:2]
            
        if response == 'wait':
            time.sleep(1)
        else:
            last_non_wait = time.time()

init_number = urllib.unquote(init_number)
call('tel:%s' % init_number, {
        'onAnswer':onAnswer,
})

urllib2.urlopen(SERVER,urllib.urlencode({'action':'end','session_id':session_id,'from':'tropo'}))

