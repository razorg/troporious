from tipfy import Rule, import_string

def get_rules(app):
    rules = [
        Rule('/conference', endpoint='conference', handler='apps.conference.handlers.RootHandler'),
        #Rule('/gcalimport/import', endpoint='gcalimport-import', handler='apps.gcalimport.handlers.ImportHandler'),
    ]
    return rules
