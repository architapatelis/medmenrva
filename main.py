import os, webapp2, jinja2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import logging


current_folder = os.path.dirname(__file__)
templates_folder = os.path.join(current_folder, 'templates')
environment = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_folder))


class Handler(webapp2.RequestHandler):
    """Used to pass templates to each class"""
    
    def write(self, *a):
        """ outputs the passed argument"""
        self.response.out.write(*a)
    
    def render_html(self, template, params):
        html = environment.get_template(template)
        return html.render(params)
    
    def display_html(self, template, values):
        self.write(self.render_html(template, values))
        

class MainPage(Handler):
    
    def get(self):
        
        user = users.get_current_user()
        if user:
            url_link = users.create_logout_url("/")
            email = user.email()
        else:
            url_link = users.create_login_url(self.request.uri)
        values = {
            "user": user,
            "url_link": url_link
            }
        self.display_html("home.html", values)
        
    


class SignUp(Handler):
    
    
    def get(self):
        self.display_html("signup.html",{})
        
        
    def post(self):
        firstname = self.request.get("firstname") 
        lastname = self.request.get("lastname")
        username = firstname + " " + lastname
        phonenumber = self.request.get("phonenumber")
        logging.info("my username is: " + username)
        
        

class Login(Handler):
    
    def get(self):
        self.display_html("login.html", {})
        

routes = [('/', MainPage),
          ('/signup', SignUp),
          ('/login', Login),
          ('/logout', Login)]

application = webapp2.WSGIApplication(routes, debug=True)


#def main():
    #run_wsgi_app(application)

#if __name__ == "__main__":
    #main()
