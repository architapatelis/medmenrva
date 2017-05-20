import os, webapp2, jinja2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import logging


current_folder = os.path.dirname(__file__)
templates_folder = os.path.join(current_folder, 'templates')
environment = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_folder))


class Handler(webapp2.RequestHandler):
    """Used to pass templates to each class"""
    def __init__(self, request=None, response=None):
        super(Handler, self).__init__(request, response)
        self.values = {}
        self.get_user_info()
        
    def write(self, *a):
        """ outputs the passed argument"""
        self.response.out.write(*a)
    
    def render_html(self, template):
        html = environment.get_template(template)
        return html.render(self.values)
    
    def display_html(self, template):
        self.write(self.render_html(template))
        
    def get_user_info(self):
        """
        Figures out if the user is logged in and fills in global variables
        if it is. If logged in, figures out if the user is signed up and 
        sets variables for user information.
        """
        self.user = users.get_current_user()
        if self.user:
            url_link = users.create_logout_url("/")
            email = self.user.email()
        else:
            url_link = users.create_login_url(self.request.uri)
            
        
        self.values["url_link"] = url_link
        self.values["user"] = self.user
    
    
    def is_user_signed_up(self):
        """
        Returns true/false whether or not the user has signed up for medmenrva
        """
        pass
    

    def is_user_logged_in(self):
        """
        Returns true/false whether or not the user is signed in or not
        """
        if self.user:
            return True
        else:
            return False
        

class MainPage(Handler):
    
    def get(self):
        self.get_user_info()
        
        self.display_html("home.html")
        
    


class SignUp(Handler):
    
    
    def get(self):
        self.display_html("signup.html")
        
        
    def post(self):
        firstname = self.request.get("firstname") 
        lastname = self.request.get("lastname")
        username = firstname + " " + lastname
        phonenumber = self.request.get("phonenumber")
        logging.info("my username is: " + username)
        
        

class Login(Handler):
    
    def get(self):
        self.display_html("login.html")
        

routes = [('/', MainPage),
          ('/signup', SignUp),
          ('/login', Login),
          ('/logout', Login)]

application = webapp2.WSGIApplication(routes, debug=True)


#def main():
    #run_wsgi_app(application)

#if __name__ == "__main__":
    #main()
