from helpers import TemplatedRequest
from google.appengine.ext import webapp, db, blobstore
from google.appengine.api import memcache, channel
from apps.validation.models import LiveSession, Recording
from django.utils import simplejson as json
import re, urllib, os, logging, time, cgi, random, string
import tropo

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
        import logging
        session_id = int(self.request.get('session_id'))
        session = LiveSession.get_by_id(session_id)
        if not session:
            logging.debug('no session with id %d' % session_id)
            return self.error(403)
        _from = self.request.get('from')
        if _from == 'tropo':
            action = self.request.get('action')
            if action == 'get_next':
                if (len(session.action_queue) == 0):
                    return self.response.out.write('wait')
                new_action = session.action_queue[0]
                session.action_queue[0:1] = []
                session.put()
                client_message = {'type':'msg','msg':'action "%s" dequeued' % new_action}
                channel.send_message(session.channel_secret, json.dumps(client_message))
                return self.response.out.write(new_action)
            elif action == 'end':
                client_message = {'type':'msg','msg':'script ended execution normally'}
                channel.send_message(session.channel_secret, json.dumps(client_message))
                #session.delete()
                return
            elif action == 'record':
                file = self.request.get('filename')
                recording = Recording(file=db.Blob(file))
                recording.put()
                session.recording_queue.append(recording.key())
                session.put()
                client_message = {'type':'recording','file_link':'/?id=%d' % recording.key().id()}
                #client_message = {'type':'recording', 'file_link':'http://www.a1freesoundeffects.com/popular12008/slap.mp3'}
                #client_message = {'type':'recording', 'file_link':'/download.wav'}
                channel.send_message(session.channel_secret, json.dumps(client_message))
                return
            elif action == 'notify':
                what = self.request.get('what')
                if what == 'timeout':
                    client_message = {'type':'msg','msg':'answer timeout has occured'}
                    channel.send_message(session.channel_secret, json.dumps(client_message))
                    return
            else:
                logging.debug('no action "%s" for server' % action)
                return self.error(402)
        elif _from == 'client':
            action = self.request.get('action')
            if not action:
                return self.error(400)
            try:
                action = json.loads(action)
            except ValueError:
                return self.error(400)
            session.action_queue.append(self.request.get('action'))
            session.put()
            client_message = {'type':'msg','msg':'answer timeout has occured'}
            channel.send_message(session.channel_secret, 'action "%s" queued' % self.request.get('action'))        
            channel.send_message(session.channel_secret, json.dumps(client_message))
            return self.response.out.write('')


class PlaygroundHandler(webapp.RequestHandler, TemplatedRequest):
    SESSION_TOKEN = '32fcb6deac2d2d4abf7d66b893c3f2cbab4c46f134f70de1d8fbece5a4a9b5ddf85aa1e3bc2b2bd7397f1353'
    def get(self):
        context = dict()
        return self.render_response('playground.html', context)

