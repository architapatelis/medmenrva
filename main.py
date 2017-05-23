import os, webapp2, jinja2
from google.appengine.api import users
import logging
from models import members
from models import medicines
import urllib 
from datetime import datetime


current_folder = os.path.dirname(__file__)
templates_folder = os.path.join(current_folder, 'templates')
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
    
    def display_html(self, template):
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
        


class MainPage(Handler):
    
    def get(self):
        if self.is_user_logged_in():
            self.member = members.Member().get_member_by_email(self.user.email())
            
            if self.member:
                self.values["member"] = self.member
        self.display_html("home.html")
        
    
class SignUp(Handler):
    
    
    def get(self):
        args = self.request.get('dest_url', None)
        if self.is_user_signed_up():
            if args:
                self.redirect(str(args))
            else:
                self.redirect('/')
                
        self.display_html("signup.html")
        
        
    def post(self):
        
        firstname = self.request.get("firstname") 
        lastname = self.request.get("lastname")
        username = firstname + " " + lastname
        phonenumber = self.request.get("phonenumber")
        logging.info("my username is: " + username)
        
        member = members.Member()
        member.firstname = firstname 
        member.lastname = lastname 
        member.phonenumber = phonenumber
        member.email = self.user.email()
        
        member.put()
        self.redirect('/')
        logging.info("user: " + username)


class MedList(Handler):
    
    def get(self):
        list_of_medicines = ""
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
        
        list_of_medicines = medicines.Medicine().get_medicines_by_member_key(self.member.key)
        self.values['medicines'] = list_of_medicines
        self.display_html('med_index.html')
        logging.info(self.member.firstname)
        logging.info(self.user)
        
        
        
class NewMed(Handler):
    def get(self):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
        self.display_html('new_med.html')
        
        
    def post(self):   
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url(False))
        name = self.request.get('medname')
        directions = self.request.get('directions')
        dosage = self.request.get('dosage')
        interval = int(self.request.get('interval'))
        quantity = int(self.request.get('quantity'))
        starttime = self.request.get('lastdosagetime')
        startdate = self.request.get('lastdosagedate')
        ampm = self.request.get('ampm')
        date_and_time_str = startdate + starttime + ampm
        timezone = self.request.get('timezone')
        member = self.member.key
        
        formated_date_time = datetime.strptime(date_and_time_str, '%Y-%m-%d%I:%M%p')
        
        medicine = medicines.Medicine()
        
        medicine.name = name 
        medicine.directions = directions
        medicine.dosage = dosage
        medicine.interval = interval
        medicine.quantity = quantity
        medicine.date_and_time = formated_date_time
        medicine.member = member
        
        
        medicine.put()
        
        self.redirect('/medicines')
        logging.info("added " + name)
        

class ShowMed(Handler):
    def get(self, med_id):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
    
        medicine_to_show = medicines.Medicine().get_medicine_by_key_id(med_id)
        
        self.values['medicine_to_show'] = medicine_to_show
        logging.info(medicine_to_show)
        self.display_html('med_show.html')
        
        

    
    
    
    
        
routes = [('/', MainPage),
          ('/signup', SignUp),
          ('/medicines', MedList),
          ('/medicines/new', NewMed),
          (r'/medicines/show/([^/]*)/?$', ShowMed)
        ]

application = webapp2.WSGIApplication(routes, debug=True)


#def main():
    #run_wsgi_app(application)

#if __name__ == "__main__":
    #main()
