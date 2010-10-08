#from gaesessions import SessionMiddleware

# suggestion: generate your own random key using os.urandom(64)
# WARNING: Make sure you run os.urandom(64) OFFLINE and copy/paste the output to
# this file.  If you use os.urandom() to *dynamically* generate your key at
# runtime then any existing sessions will become junk every time you start,
# deploy, or update your app!
import os
COOKIE_KEY = '\xc8\xa6\xfa\x8b\xd6RT#7\x0bHz\xbd\x88\xdcv\xc1\xf7}\xf3P\xce\x83\x04>\x8cw0\x12:\x14m\xecS\xac\xc7\x0c\xed+c\xcdB\x8218a\xd9>\xa3\xfeVSB\xdaLG/@\xa4K\xcb\xe3\x19\xf7'

def webapp_add_wsgi_middleware(app):
  #app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
  return app
