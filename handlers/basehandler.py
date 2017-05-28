import os, webapp2, jinja2
from google.appengine.api import users
from models import members
import urllib
import re




current_folder = os.path.dirname(__file__)
templates_folder = os.path.join(current_folder, '..', 'templates')
environment = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_folder))


class Handler(webapp2.RequestHandler):
    """Used to pass templates to each class"""
    
    def __init__(self, request=None, response=None):
        super(Handler, self).__init__(request, response)
        
        self.values = {}
        self.logout_link = users.create_logout_url("/")
        self.values['logout_link'] = self.logout_link
        self.login_link = users.create_login_url(self.request.uri)
        self.values['login_link'] = self.make_login_url()
        self.user = users.get_current_user()
        self.values['user'] = self.user
        
       
        
    def write(self, *a):
        """ outputs the passed argument"""
        self.response.out.write(*a)
    
    def render_html(self, template):
        html = environment.get_template(template)
        return html.render(self.values)
    
    def display_html(self, template, **params):
        self.write(self.render_html(template))


    def make_login_url(self, to_create_profile=True):
        if to_create_profile:
            args = {'dest_url': self.request.uri}
            return users.create_login_url("/signup" + '?' +\
                                          urllib.urlencode(args))
        else:
            return users.create_login_url(self.request.uri)
        
    def get_user_info(self):
    
        """Figures out if the user is logged in and fills in global variables
        if it is. If logged in, figures out if the user is signed up and 
        sets variables for user information."""
        
        self.user = users.get_current_user()
        self.values["user"] = self.user
    
    
    def is_user_signed_up(self):
        """
        Returns true/false whether or not the user has signed up for memenrva
        """
        if self.is_user_logged_in():
            self.member = members.Member().get_member_by_email(self.user.email())
            
            if self.member:
                self.values["member"] = self.member
                return True
        return False


    def is_user_logged_in(self):
        """
        Returns true/false whether or not the user is signed in or not into their google account
        """
        if self.user:
            return True
        else:
            return False
        
    def add_member_key_to_values_dict(self): 
        if self.is_user_logged_in():
            self.member = members.Member().get_member_by_email(self.user.email())
            
            if self.member:
                self.values["member"] = self.member
    
    def valid_name(self, medname):
        medname_re = re.compile(r"^[a-zA-Z- ]*$")
        return (medname if medname_re.match(medname) else False)
                
    def valid_phonenumber(self, phonenumber):
        phonenumber_re = re.compile(r"^[0-9- ]*$")
        return (phonenumber if phonenumber_re.match(phonenumber) else False)

    