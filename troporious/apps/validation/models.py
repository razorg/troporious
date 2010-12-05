from google.appengine.ext import db

class ServiceUser(db.Model):
  ### KEY IS API_KEY ###
  #api_key = db.StringProperty(required=True)#
  name = db.StringProperty(required=True)

class LiveSession(db.Model):
  ### ID is session_id ###
  dispached = db.BooleanProperty(required=True)
  channel_secret = db.StringProperty(required=True)
  action_queue = db.ListProperty(str)

class ValidationRequest(db.Model):
  ### KEY IS ACCESS_KEY ###
  target = db.TextProperty(required=True)
  api_key = db.TextProperty(required=True)
  #access_key = db.TextProperty(required=True)
  secret = db.IntegerProperty(required=True)
  result = db.TextProperty()
  date_submit = db.DateProperty()
  date_expire = db.DateProperty()  
  
class DemoClient(db.Model):
  ## KEY is ip as str. ###
  times = db.IntegerProperty(required=True, default=0)

class Recording(db.Model):
  file_upload = db.BlobProperty()

class File(db.Model):
    file = db.BlobProperty()
