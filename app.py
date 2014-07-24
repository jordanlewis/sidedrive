import webapp2
import json

from model import Account, Info
from backends import NullBackend
from twitter_backend import TwitterBackend

DEFAULT_SERVICE = "Twitter"
BACKENDS = {
    "NULL": NullBackend(),
    "Twitter": TwitterBackend(),
}

def _get_default_account():
    default = Account.query(Account.username==DEFAULT_NAME,
                            Account.password==DEFAULT_PW,
                            Account.service==DEFAULT_SERVICE).get()
    if default:
        return default
    else:
        default_key = Account(username=DEFAULT_NAME,
                              password=DEFAULT_PW,
                              service=DEFAULT_SERVICE).put()
        return default_key.get()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class Store(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)

    def get(self):
        backend = BACKENDS[DEFAULT_SERVICE]
        title = self.request.get('title')
        # no user-specific storage
        inf = Info.query(Info.title == title).get()
        if inf is None:
            self.response.write('data with title {} not found'.format(title))
            return
        val = backend.get(inf.refs)
        self.response.write(val)

    def post(self):
        vals = self.request.POST
        title = vals.get('title')
        data = vals.get('info')
        if not (title and data):
            self.response.write('incomplete or empty data sent')
            return
        backend = BACKENDS[DEFAULT_SERVICE]
        info = Info(title=title, backend=DEFAULT_SERVICE,
                    refs=[backend.store(data)]).put()
        self.response.write('stored')

class List(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'application/json'
        self.response.write(json.dumps({'titles': [i.title for i in Info.query()]}))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/drive/list', List),
    ('/drive', Store),
], debug=True)
