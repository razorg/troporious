from google.appengine.ext import db

class LiveSession(db.Model):
  ### ID is session_id ###
  dispached = db.BooleanProperty(required=True)
  channel_secret = db.StringProperty(required=True)
  action_queue = db.ListProperty(str)
  recording_queue = db.ListProperty(db.Key)

class Recording(db.Model):
  file = db.BlobProperty()

