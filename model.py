from google.appengine.ext import ndb

class Account(ndb.Model):
    """An account used for storing side data"""
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    service = ndb.StringProperty()

class Info(ndb.Model):
    """A single value"""
    title = ndb.StringProperty()
    account = ndb.StructuredProperty(Account)
    refs = ndb.StringProperty(repeated=True)
