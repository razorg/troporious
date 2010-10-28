def onAnswer(event):
    say(text, {"voice":voice})
    hangup()

call(number, {
        "onAnswer":onAnswer,
        #"onCallFailure":onCallFailure,
        #"onError":onError,
        #"onTimeout":onTimeout,
    })
