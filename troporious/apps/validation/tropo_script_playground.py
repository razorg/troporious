def onTransferSuccess(event):
    say(_transfer["text"], {"voice":voice})
    hangup()

def onAnswer(event):
    say(text, {"voice":voice})
    if _tranfer["need"] == "yes":
        transfer(_transfer["number"], {
                'onSuccess':onTransferSuccess,
                #'onCallFailure':onTransferFailure,
                #'onTimeout':onTransferTimeout
        })
    else:
        hangup()

call(number, {
        "onAnswer":onAnswer,
        #"onCallFailure":onCallFailure,
        #"onError":onError,
        #"onTimeout":onTimeout,
    })
