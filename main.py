from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


class SignUp(webapp.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<b>Sign Up</b>')


routes = [('/', MainPage),
          ('/signup', SignUp)]
application = webapp.WSGIApplication(routes, debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
