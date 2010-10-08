from tipfy import Rule, import_string

def get_rules(app):
    rules = [
        Rule('/', endpoint='hello-world', handler='handlers.RootHandler'),
        Rule('/google-contacts', endpoint='hello-world', handler='handlers.GoogleContactsHandler'),
        
    ]
    for app_module in app.get_config('tipfy', 'apps_installed'):
        app_rules = import_string('%s.urls' % app_module)
        rules.extend(app_rules.get_rules(app))
    return rules
