from helpers import TemplatedRequest
from google.appengine.ext import webapp, db, blobstore
from google.appengine.api import memcache, channel
from apps.validation.models import LiveSession, ValidationRequest, Recording, ServiceUser, DemoClient, File
from django.utils import simplejson as json
import re, urllib, os, logging, time, cgi, random, string
import tropo

HOSTNAME = "http://2.latest.smsandvoice.appspot.com/playground/download_audio"
SECRET_LEN = 10

class PlaygroundLiveHandler(webapp.RequestHandler):
    def get(self):
        context = dict()
        channel_secret = ''.join(random.choice(string.letters) for i in xrange(SECRET_LEN))
        token = channel.create_channel(channel_secret)
        context['channel_token'] = token
        new_session = LiveSession(dispached=False,channel_secret=channel_secret)
        new_session.put()
        number = self.request.get('number')
        tropo.tropo_run_script({'session_id':new_session.key().id(),'init_number':number})
        
        response = {'channel_token':token, 'session_id':new_session.key().id()}
        return self.response.out.write(json.dumps(response))
        
    def post(self):
        session_id = int(self.request.get('session_id'))
        session = LiveSession.get_by_id(session_id)
        _from = self.request.get('from')
        if _from == 'tropo':
            action = self.request.get('action')
            if action == 'get_next':
                if (len(session.action_queue) == 0):
                    return self.response.out.write('wait')
                new_action = session.action_queue[0]
                session.action_queue[0:1] = []
                session.put()
                channel.send_message(session.channel_secret, 'action "%s" dequeued' % new_action)
                return self.response.out.write(new_action)
            elif action == 'end':
                channel.send_message(session.channel_secret, 'script ended')
                session.delete()
        elif _from == 'client':
            action = self.request.get('action')
            if not action:
                return self.error(400)
            if action == 'exec':
                code = self.request.get('code')
                if not code:
                    return self.error(400)
                try:
                    code = json.loads(code)
                except ValueError:
                    return self.error(400)
                session.action_queue.append(code)
                session.put()
            channel.send_message(session.channel_secret, 'aciont "%s" queued' % code)

class PlaygroundHandler(webapp.RequestHandler, TemplatedRequest):
    SESSION_TOKEN = '32fcb6deac2d2d4abf7d66b893c3f2cbab4c46f134f70de1d8fbece5a4a9b5ddf85aa1e3bc2b2bd7397f1353'
    def get(self):
        context = dict()
        return self.render_response('playground.html', context)

