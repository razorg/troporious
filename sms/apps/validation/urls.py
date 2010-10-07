from tipfy import Rule, import_string

def get_rules(app):
    rules = [
      Rule('/validator', endpoint='validator', handler='apps.validation.handlers.ValidatorHandler'),
      Rule('/validate', endpoint='validate', handler='apps.validation.handlers.ValidateHandler'),
      Rule('/validator/BackendResponse', endpoint='BackendResponse', handler='apps.validation.handlers.BackendResponseHandler'),
      Rule('/validator/demo', endpoint='validator-demo', handler='apps.validation.handlers.ValidatorDemoHandler'),
    ]
    return rules
