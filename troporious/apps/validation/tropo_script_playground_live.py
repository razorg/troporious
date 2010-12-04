import urllib, urllib2, time

SERVER = 'http://2.latest.smsandvoice.appspot.com/playground-live'
wait_times = 15

def logger(string):
    log('LOGGED : %s' % string)

def do_next_command():
    response = urllib2.urlopen(SERVER, urllib.urlencode({'action':'get_next','session_id':session_id,'from':'tropo','channel_token':channel_token}))
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


while wait_times != 0:
    wait_times = wait_times - 1
    response = do_next_command()
    if response == 'wait':
        time.sleep(5)
