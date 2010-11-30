def logger(string):
  log("LOGGED : "+string)

def onTransferSuccess(event):
    #say(transferrtext, {"voice":voice})
    hangup()

def onAnswer(event):
    if conf_id != "None":
        conference(conf_id, {"terminator":"#"})
        hangup()
    else:
        say(text, {"voice":voice})
        if audio_url != 'None':
            say(audio_url)
        if transferr == "yes":
            transfer(transferrnumber, {
                    'callerID':transferrcallerid,
                    'onSuccess':onTransferSuccess,
                    #'onCallFailure':onTransferFailure,
                    #'onTimeout':onTransferTimeout
            })
        else:
            hangup()

logger(str(currentCall))
call(number, {
        "onAnswer":onAnswer,
        "callerID":callerid,
        #"onCallFailure":onCallFailure,
        #"onError":onError,
        #"onTimeout":onTimeout,
    })
