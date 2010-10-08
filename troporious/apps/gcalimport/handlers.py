from tipfy import RequestHandler, Response, abort
from tipfy.ext.jinja2 import render_response
from tipfy.ext.auth.facebook import FacebookMixin
from tipfy.ext.session import SessionMiddleware, SessionMixin
import gdata.gauth
import pickle
from gdata import client
from gdata.calendar import service
from datetime import datetime
import atom
import re

CONSUMER_KEY = 'smsandvoice.appspot.com'
CONSUMER_SECRET = 'Hhqc8FYI9rbdd1aGyv+xPasT'
SCOPE = ['http://www.google.com/calendar/feeds/']

class RootHandler(RequestHandler):
    def get(self, **kwargs):
        return render_response('gcalimport.html', message={})

class ImportHandler(RequestHandler, SessionMixin, FacebookMixin):
    middleware = [SessionMiddleware]
    def get(self, **kwargs):
        if self.request.args.get('session'):
            self.get_authenticated_user(callback=self._save_uid)
            return self.redirect('/gcalimport/import')
            
        session = self.get_session()
        fb_session_key = session.get('fb_session_key')
        if not fb_session_key:
            return self.authenticate_redirect(callback_uri='/gcalimport/import',cancel_uri='cancel',extended_permissions=['friends_birthday'])
        #is authed from facebook now.

        oauth_token = self.request.args.get('oauth_token')
        if not session.get('access_token'):
            myclient = client.GDClient()
            if not oauth_token:
                request_token = myclient.GetOAuthToken(SCOPE, self.request.url, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
                session['request_token'] = request_token
                authorization_url = request_token.generate_authorization_url()
                return self.redirect(str(authorization_url))
            else:
                request_token_saved = session.get('request_token')
                request_token = gdata.gauth.AuthorizeRequestToken(request_token_saved, self.request.url)
                myclient.GetAccessToken(request_token)
                session['access_token'] = request_token
                return self.redirect('/gcalimport/import')
            
        return self._import()
        
    def _save_uid(self, response):
        if not response:
            raise 'no response!!'
        session = self.get_session()
        session['fb_session_key'] = response['session_key']
        session['fb_uid'] = response['uid']
    
    def _get_friends(self, response):
        if response is None:
            raise 'no response!!'
        return response

    def _get_birthdays(self, response):
        if response is None:
            raise ' no response!!'
        return response

    def _import(self):
        fb_session_key = self.session.get('fb_session_key')
        friend_list = self.facebook_request('friends.get', callback=self._get_friends, session_key=fb_session_key)
        friend_list_comma = ''
        for friend in friend_list:
            friend_list_comma += str(friend)+','
        birthdays = self.facebook_request('users.getInfo', callback=self._get_birthdays, session_key=fb_session_key, uids=friend_list_comma, fields=['birthday,name'])
        
        gogl_access_token = self.session.get('access_token')
        cal_service = service.CalendarService()
        cal_service.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
        oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
        oauth_token = gdata.auth.OAuthToken(key=gogl_access_token.token, secret=gogl_access_token.token_secret, scopes=SCOPE, oauth_input_params=oauth_input_params) 
        cal_service.SetOAuthToken(oauth_token)
        
        response = ''
        p = re.compile(r'\d+ \w+')
        next_year = str(datetime.today().year + 1)
        for birthday in birthdays:
            if birthday['birthday'] is None:
                continue
            birth_date = birthday['birthday']
            name = birthday['name']
            birthday_event = gdata.calendar.CalendarEventEntry()
            birthday_event.title = atom.Title('birthday - ' + name)
            birthday_event.content = atom.Content('something')
            regex_result = p.match(birth_date)
            if regex_result is None:
                raise 'no match!'
            birth_date = regex_result.group(0)
            date = datetime.strptime(birth_date, '%d %B')
            date_end = date.replace(hour=date.hour+1)
            start_time = next_year + date.strftime('-%m-%dT%H:00:00.000Z')
            end_time = next_year + date_end.strftime('-%m-%dT%H:00:00.000Z')
            #response += start_time + ' ' + end_time + '<br />' +  '\n'
            birthday_event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
            
            new_event = cal_service.InsertEvent(birthday_event, '/calendar/feeds/default/private/full')
            
            print 'New single event inserted: %s' % (new_event.id.text,)
            print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
            print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)
            raise ''
        return Response(response)
        
        
