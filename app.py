import webapp2

import model
from backends import NullBackend

DEFAULT_SERVICE = "NULL"
DEFAULT_NAME = "sidedrive"
DEFAULT_PW = "drivin"
BACKENDS = {
    "NULL": NullBackend,
}

def __get_default_account():
    default = Account.query(Account.username==DEFAULT_NAME,
                            Account.password==DEFAULT_PW,
                            Account.service==DEFAULT_SERVICE).get()
    if default:
        return default
    else:
        default_key = Account(DEFAULT_NAME, DEFAULT_PW, DEFAULT_SERVICE).put()
        return default_key.get()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class Store(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self.account = __get_default_account()

    def get(self):
        backend = BACKENDS[self.account.service]
        title = self.request.get(title)
        # no user-specific storage
        inf = Info.query(Info.title == title).get()
        val = backend.get(self.account.username, self.account.password, inf.refs)
        self.response.write(val)

    def post(self):
        vals = self.request.POST
        title = vals.get('title')
        data = vals.get('info')
        if not (title and data):
            return
        backend = BACKENDS[self.account.service]
        info = model.Info(title, self.account,
                          backend.store(self.account.username, self.account.password, data)).put()
        self.response.write('stored')

class List(webapp2.RequestHandler):
    def get(self):
        pass

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/drive/list', List),
    ('/drive', Store),
], debug=True)
