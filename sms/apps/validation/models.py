from google.appengine.ext import db

class ServiceUser(db.Model):
  name = db.StringProperty(required=True)
  api_key = db.StringProperty(required=True)
  

class ValidationRequest(db.Model):
  target = db.StringProperty(required=True)
  api_key = db.StringProperty(required=True)
  access_key = db.StringProperty(required=True)
  secret = db.IntegerProperty(required=True)
  pending = db.BooleanProperty()
  date_submit = db.DateProperty()
  date_expire = db.DateProperty()
