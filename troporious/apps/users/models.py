from google.appengine.ext import db


class User(db.Model):
    ### key_name is user id ###
    username = db.StringProperty(required=True);
    password = db.StringProperty(required=True);
    create_date = db.StringProperty(required=True);
    api_key = db.StringProperty(required=True);
