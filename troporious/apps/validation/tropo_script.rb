require 'net/http'
require 'uri'
require 'cgi'
require 'json'

SERVER = 'http://4.smsandvoice.appspot.com/transcript-callback'
$threads = []
$running = true

def logger(string)
    log("LOGGED : #{string}")
end

def recordWithInterval()
    while $running
        startCallRecording(SERVER+'?from=tropo&session_id='+$session_id+'&action=record', {:format => 'audio/mp3'})
        sleep(2);
        stopCallRecording()
    end
end
    

def send_message(context)
    logger(context.to_s)
    context['from'] = 'tropo'
    context['session_id'] = $session_id
    begin
        response = Net::HTTP.post_form(URI.parse(SERVER), context)
    rescue => msg
        logger('wtf happened here? ' + msg)
        return 'wait'
    end
    
    if response.code == '500' || response.code == '400'
        logger('WTF SERVER_ERROR')
        raise 'server_error'
    end
    return response
end

def onChoice(event)
    logger("you said " + event.value)
    say(event.value)
end

def do_next_command()
    response = send_message({ 'action' => 'get_next' }).body()
    logger(response)
    if response == 'wait'
        logger('WAITING')
        return response
    end
    response = JSON.parse(response)
    if response['action'] == 'exec'
        eval(response['code'])
    elsif response['action'] == 'say'
        say(response['text'])
    elsif response['action'] == 'ask'
        record("Spit some crap", {
                :beep => true,
                :terminator => "#",
                :onRecord => lambda { |event|
                    say('recorded')
                },
                :transcriptionOutURI => SERVER+'?from=tropo&session_id='+$session_id+'&action=transcript'
        })
    end
end
 
def onAnswer(e)
    if $live_audio == 'true'
        recorders = Thread.new { recordWithInterval() }
    end
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
    $running = false
    send_message({'action' => 'end'})
    recorders.wait
end

def onTimeout(e)
    send_message({'action' => 'notify', 'what' => 'timeout'})
end

call('tel:'+$init_number, { :onAnswer => method(:onAnswer), :onTimeout => method(:onTimeout), :timeout => 30 })
