require 'net/http'
require 'uri'
require 'cgi'
require 'json'

SERVER = 'http://3.latest.smsandvoice.appspot.com/playground-live'

def logger(string)
    log("LOGGED : #{string}")
end

def send_message(context)
    context['from'] = 'tropo'
    context['session_id'] = $session_id
    response = Net::HTTP.post_form(URI.parse(SERVER), context)
    if response.code == '500' || response.code == '400'
        raise 'server_error'
    end
    return response
end

def do_next_command()
    response = send_message({ 'action' => 'get_next' }).body()
    logger(response)
    if response == 'wait'
        logger('WAITING')
        return response
    end
    response = JSON.parse(response)
    if response['method'] == 'exec'
        eval(response)
    elsif response['method'] == 'say'
        say(response['text'])
    end
end
 
def onAnswer(e)
    say('Hello! I\'m your servant.')
    last_non_wait = Time.now.to_i
    while last_non_wait + 30 > Time.now.to_i
        response = do_next_command()
        if response == "wait"
            sleep(1)
        else
            last_non_wait = Time.now.to_i
        end
    end
end

#init_number = CGI.unescape($init_number)
call('tel:+302810322628', { :onAnswer => method(:onAnswer) })
