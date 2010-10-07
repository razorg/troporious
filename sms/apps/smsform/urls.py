from tipfy import Rule, import_string

def get_rules(app):
    rules = [Rule('/testform', endpoint='testform', handler='apps.smsform.handlers.TestFormHandler'),
    ]
    return rules
