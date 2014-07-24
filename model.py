from google.appengine.ext import ndb

class Info(ndb.Model):
    """A single value"""
    title = ndb.StringProperty()
    account = ndb.StructuredProperty(Account)
    refs = ndb.StringProperty(repeated=True)

class Account(ndb.Model):
    """An account used for storing side data"""
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    service = ndb.StringProperty()
