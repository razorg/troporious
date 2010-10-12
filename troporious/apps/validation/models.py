from google.appengine.ext import db

class ServiceUser(db.Model):
  ### KEY IS API_KEY ###
  #api_key = db.StringProperty(required=True)#
  name = db.StringProperty(required=True)
  

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
  
