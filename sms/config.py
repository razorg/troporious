# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration settings.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""
config = {}
config['tipfy.ext.auth.facebook'] = {
    'api_key':    'c9e89ebd191c8884ec4991543e0770d5',
    'app_secret': '390d7250172affda4057dce897552e37',
}
config['tipfy.ext.session'] = {
    'secret_key': 'vbj0j03432$#()*$@#dzDSA',
}

config['tipfy.ext.auth.twitter'] = {
    'consumer_key':    '8mXmrfHffAQthmtyDmGQ',
    'consumer_secret': 'hQJiRlzZY6xyxHSougXpWQOpuRH0EvAgPvOwlVtMmI',
}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
    # Enable debugger. It will be loaded only in development.
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
    ],
    # Enable the Hello, World! app example.
    'apps_installed': [
        'apps.smsform',
        'apps.openid',
        'apps.gcalimport',
        'apps.conference',
        'apps.validation',
    ],
}
