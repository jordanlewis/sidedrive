from google.appengine.ext import ndb

class Account(ndb.Model):
    """An account used for storing side data"""
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    backend = ndb.StringProperty()

class Info(ndb.Model):
    """A single value"""
    title = ndb.StringProperty()
    backend = ndb.StringProperty()
    refs = ndb.StringProperty(repeated=True)
