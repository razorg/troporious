from helpers import TemplatedRequest
from google.appengine.ext import webapp, db
from apps.validation.models import LiveSession, Recording
class RootHandler(webapp.RequestHandler, TemplatedRequest):
    def get(self):
        recording_id = self.request.get('id')
        if not recording_id:
            sessions = LiveSession.all().fetch(100)
            for session in sessions:
                self.response.out.write('session(%d) : ' % session.key().id())
                recordings = db.get(session.recording_queue)
                for recording in recordings:
                    self.response.out.write('<a href="/?id=%s">%s</a> ' % (recording.key().id(), recording.key().id()))
                self.response.out.write('<br>')
            return self.response.out.write('</body></html>')
        
        self.response.headers["Content-Type"] = 'audio/mp3'
        recording = Recording.get_by_id(int(recording_id))
        return self.response.out.write(recording.file)
