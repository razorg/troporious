from tipfy import Rule, import_string

def get_rules(app):
    rules = [
        Rule('/testopenid', endpoint='testopenid', handler='apps.openid.handlers.TestOpenIDHandler'),
        Rule('/login', endpoint='openid-login', handler='apps.openid.handlers.OpenIDLogin'),
        Rule('/login-facebook', endpoint='openid-login-facebook', handler='apps.openid.handlers.FacebookLoginHandler'),
        Rule('/login-google', endpoint='openid-login-google', handler='apps.openid.handlers.GoogleLoginHandler'),
        Rule('/login-twitter', endpoint='openid-login-google', handler='apps.openid.handlers.TwitterLoginHandler'),
        
    ]
    return rules
