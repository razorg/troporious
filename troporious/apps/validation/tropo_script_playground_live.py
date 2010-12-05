import urllib, urllib2, time

SERVER = 'http://2.latest.smsandvoice.appspot.com/playground-live'
end_time = int(time.time()) + 30

def logger(string):
    log('LOGGED : %s' % string)

def do_next_command():
    response = urllib2.urlopen(SERVER, urllib.urlencode({'action':'get_next','session_id':session_id,'from':'tropo'}))
    response = urllib.unquote(response.read())
    logger(str(response))
    if response == 'wait':
        logger('WAITING')
        return response
    response = response.split(',')
    response_dict = dict()
    for item in response:
         items = item.split(':')
         response_dict[items[0]] = items[1]
    logger(str(response) + '     ' +str(response_dict))
    if response_dict['method'] == 'call':
        call('tel:%s' % response_dict['num'])
    else:
        logger('UNKNOWN METHOD "%s"' % response_dict['method'])


while time.time() < end_time:
    response = do_next_command()
    if response == 'wait':
        time.sleep(1)

urllib2.urlopen(SERVER,urllib.urlencode({'action':'end','session_id':session_id,'from':'tropo'}))

