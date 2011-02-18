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

$will_record = false

def onTranscriptStartChoice(event)
    logger("onchoice")
    say("you said " + event.attempt)
    $will_record = true
end

def TranscriptThread()
    while $running
        ask("press 9 to record", {
                :choices => "[1 DIGITS]",
                :mode => "dtmf",
                :onChoice => method(:onTranscriptStartChoice)
        })
        if $will_record
            $will_record = false
            record("", {
                    :beep => true,
                    :terminator => "#",
                    :onRecord => lambda { |event|
                        say('ok')
                    },
                    :transcriptionOutURI => SERVER+'?from=tropo&session_id='+$session_id+'&action=transcript'
            })
        end
    end
end
        
    

def onChoice(event)
    logger("you said " + event.value.confidence)
    
    say(event.value)
end

def do_next_command()
    response = send_message({ 'action' => 'get_next' }).body()
    logger(response)
    if response == 'wait'
        return response
    end
    response = JSON.parse(response)
    if response['action'] == 'end1_msg'
        say(response['msg'])
    elsif response['action'] == ''
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
    say('This text....')
    recorder = Thread.new { TranscriptThread() }
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
    recorder.wait
end

def onTimeout(e)
    send_message({'action' => 'notify', 'what' => 'timeout'})
end

call('tel:'+$init_number, { :onAnswer => method(:onAnswer), :onTimeout => method(:onTimeout), :timeout => 30 })
