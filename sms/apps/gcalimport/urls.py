from tipfy import Rule, import_string

def get_rules(app):
    rules = [
        Rule('/gcalimport', endpoint='gcalimport', handler='apps.gcalimport.handlers.RootHandler'),
        Rule('/gcalimport/import', endpoint='gcalimport-import', handler='apps.gcalimport.handlers.ImportHandler'),
    ]
    return rules
