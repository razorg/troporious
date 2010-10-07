from tipfy import RequestHandler, Response
from tipfy.ext.jinja2 import render_response
################################################
import gdata.gauth
import gdata.docs.client
import tipfy
from tipfy.ext.session import SessionMiddleware, SessionMixin
import pickle
from gdata.contacts import client
from gdata.contacts import service
class RootHandler(RequestHandler):
    def get(self, **kwargs):
        return render_response('root.html', message='Hello, Jinja!')


CONSUMER_KEY = 'smsandvoice.appspot.com'
CONSUMER_SECRET = 'Hhqc8FYI9rbdd1aGyv+xPasT'
SCOPE = ['http://www.google.com/m8/feeds/']

 
class GoogleContactsHandler(RequestHandler, SessionMixin):
    middleware = [SessionMiddleware]
    
    def get(self, **kwargs):
        myclient = client.ContactsClient()
        oauth_token = self.request.args.get('oauth_token')
        if not oauth_token:
            request_token = myclient.GetOAuthToken(SCOPE, self.request.url, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            self.session['request_token'] = pickle.dumps(request_token)
            #return Response('dsadas')
            authorization_url = request_token.generate_authorization_url()
            return tipfy.redirect(str(authorization_url))
        
        request_token_saved_str = self.session.get('request_token')
        request_token_saved = pickle.loads(request_token_saved_str)
        request_token = gdata.gauth.AuthorizeRequestToken(request_token_saved, self.request.url)
        myclient.GetAccessToken(request_token)
        docs_service = service.ContactsService()
        docs_service.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
        oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET) 
        oauth_token = gdata.auth.OAuthToken(key=request_token.token, secret=request_token.token_secret, scopes=SCOPE, oauth_input_params=oauth_input_params) 
        docs_service.SetOAuthToken(oauth_token)
        feed = docs_service.GetContactsFeed()
        PrintFeed(feed)
        return Response('')

def PrintFeed(feed):
  for i, entry in enumerate(feed.entry):
    print '\n%s %s' % (i+1, entry.title.text)
    if entry.content:
      print '    %s' % (entry.content.text)
    # Display the primary email address for the contact.
    for email in entry.email:
      if email.primary and email.primary == 'true':
        print '    %s' % (email.address)
    # Show the contact groups that this contact is a member of.
    for group in entry.group_membership_info:
      print '    Member of group: %s' % (group.href)
    # Display extended properties.
    for extended_property in entry.extended_property:
      if extended_property.value:
        value = extended_property.value
      else:
        value = extended_property.GetXmlBlobString()
      print '    Extended Property - %s: %s' % (extended_property.name, value)
