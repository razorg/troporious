from tipfy import RequestHandler, Response, abort
from tipfy.ext.jinja2 import render_response
from tipfy.ext.auth.openid import OpenIdMixin
from tipfy.ext.auth.facebook import FacebookMixin
from tipfy.ext.session import SessionMiddleware, FlashMixin, CookieMixin, SessionMixin
from tipfy.ext.auth.google import GoogleMixin
from tipfy.ext.auth.twitter import TwitterMixin

class TestOpenIDHandler(RequestHandler):
    def get(self, **kwargs):
        return render_response('login.html', message={})
        
class OpenIDLogin(RequestHandler, OpenIdMixin, FlashMixin):
    middleware = [SessionMiddleware]
    def get(self, **kwargs):
        if self.request.args.get('openid.mode', None):
            endpoint = self.get_flash()[0]
            return self.get_authenticated_user(self._on_auth, openid_endpoint=endpoint)
        endpoint = self.request.args.get('identifier')
        if not endpoint:
            return Response('no endpoint set on parameter')
        self.set_flash(endpoint)
        return self.authenticate_redirect(openid_endpoint=endpoint)

    def _on_auth(self, user):
        if not user:
            abort(403)
        return Response(str(user))
        
        
class FacebookLoginHandler(RequestHandler, FacebookMixin, SessionMixin):
    middleware = [SessionMiddleware]
    def head(self, **kwargs):
        """Facebook pings this URL when a user first authorizes your application."""
        return Response('')
        
    def get(self):
        method = self.request.args.get('method', None)
        if method:
            return self.facebook_request(method, self._callback, session_key=self.session.get('fb_session_key'))
            
            
        if self.request.args.get('session', None):
            return self.get_authenticated_user(self._on_auth)
        
        extended = self.request.args.getlist('extended_parameters', None)
        return self.authenticate_redirect(extended_permissions=extended, cancel_uri="/login-facebook?result=cancel")
    
    def _on_auth(self, user):
        if not user:
            abort(403)
        
        self.session['fb_session_key'] = user['session_key']
        return Response(str(user))
     
    def _callback(self, response):
         if not response:
             return Response('no response. maybe not authed?')
             
         return Response(str(response))

class GoogleLoginHandler(RequestHandler, GoogleMixin):
    def get(self):
        if self.request.args.get('openid.mode', None):
            return self.get_authenticated_user(self._on_auth)
        return self.authenticate_redirect()
        
    def _on_auth(self, user):
        if not user:
            abort(403)
        return Response(str(user))

class TwitterLoginHandler(RequestHandler, CookieMixin, TwitterMixin):
    middleware = [SessionMiddleware]
    def get(self):
        if self.request.args.get('oauth_token', None):
            return self.get_authenticated_user(self._on_auth)
        return self.authorize_redirect()
        
    def _on_auth(self, user):
        if not user:
            abort(403)
        return Response(str(user))
