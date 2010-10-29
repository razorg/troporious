def onTransferSuccess(event):
    #say(transferrtext, {"voice":voice})
    hangup()

def onAnswer(event):
    if conf_id != "None":
        conference(conf_id, {"terminator":"#"})
        hangup()
    else:
        say(text, {"voice":voice})
        if transferr == "yes":
            transfer(transferrnumber, {
                    'onSuccess':onTransferSuccess,
                    #'onCallFailure':onTransferFailure,
                    #'onTimeout':onTransferTimeout
            })
        else:
            hangup()

call(number, {
        "onAnswer":onAnswer,
        "callerID":callerid,
        #"onCallFailure":onCallFailure,
        #"onError":onError,
        #"onTimeout":onTimeout,
    })
