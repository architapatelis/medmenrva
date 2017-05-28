import webapp2
import logging
from models import members
from models import medicines
import arrow
from handlers import Handler


class MainPage(Handler):
    
    def get(self):
        self.add_member_key_to_values_dict()
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
        
        
        have_error = False
        valid_firstname = self.valid_name(firstname)
        valid_lastname = self.valid_name(lastname)
        valid_phonenumber = self.valid_phonenumber(phonenumber)
        
        
        if not valid_firstname:
            have_error = True
            self.values['error_firstname'] = 'This is not a valid first name'
        if not valid_lastname:
            have_error = True
            self.values['error_lastname'] = "This is not a valid last name"
        if not valid_phonenumber:
            have_error = True
            self.values['error_phonenumber'] = "This is not a valid phone number"
            
            
        if have_error:
            self.display_html('signup.html')
        else:
            member = members.Member()
            member.firstname = firstname 
            member.lastname = lastname 
            member.phonenumber = phonenumber
            member.email = self.user.email()
            
            saved_member = member.put()
            
            if saved_member:
                    self.values['display_message'] = member.firstname + " welcome to Medmenrva!"
                    self.display_html('message.html')
                
        
        logging.info("user: " + username)


class MedList(Handler):
    
    def get(self):
        #list_of_medicines = ""
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
        
        
        
        self.values['medname'] = name = self.request.get('medname')
        directions = self.request.get('directions')
        dosage = int(self.request.get('dosage'))
        interval = int(self.request.get('interval'))
        quantity = int(self.request.get('quantity'))
        starttime = self.request.get('lastdosagetime')
        startdate = self.request.get('lastdosagedate')
        ampm = self.request.get('ampm')
        date_and_time_str = startdate + starttime + ampm
        timezone = self.request.get('timezone')
        member = self.member.key
        
        formated_date_time = arrow.Arrow.strptime(date_and_time_str, '%Y-%m-%d%I:%M%p', timezone)
        date_time_to_utc = formated_date_time.to('utc')
        
        have_error = False
        valid_name = self.valid_name(name)
        
        if not valid_name:
            have_error = True
            self.values['error_name'] = 'That was not a valid name'
            
            
        if have_error:
            self.display_html('new_med.html')
        else:
            medicine = medicines.Medicine()
            
            medicine.name = name 
            medicine.directions = directions
            medicine.dosage = dosage
            medicine.interval = interval
            medicine.quantity = quantity
            medicine.date_and_time = date_time_to_utc.naive
            medicine.member = member
            
            
            saved_med = medicine.put()
            logging.info(saved_med)
            
            if saved_med:
                self.values['display_message'] = medicine.name + " was saved successfully!"
                self.display_html('message.html')
            
        logging.info("added " + name)
        

class ShowMed(Handler):
    def get(self, med_id):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
    
        medicine_to_show = medicines.Medicine().get_medicine_by_key_id(med_id)
        
        self.values['medicine_to_show'] = medicine_to_show
        self.display_html('med_show.html')
        
        
        
        

class EditMed(Handler):
    def get(self, med_id):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
        
        medicine_to_edit = medicines.Medicine().get_medicine_by_key_id(med_id)
        self.values['medicine_to_edit'] = medicine_to_edit
        
        self.display_html('med_edit.html')
    
    def post(self, med_id):  
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url(False))
            
        
        medicine_to_edit = medicines.Medicine().get_medicine_by_key_id(med_id)
        
        self.values['medicine_to_edit'] = medicine_to_edit
        
        self.values['medname'] = name = self.request.get('medname')
        directions = self.request.get('directions')
        dosage = int(self.request.get('dosage'))
        interval = int(self.request.get('interval'))
        
        have_error = False
        valid_name = self.valid_name(name)
        
        if not valid_name:
            have_error = True
            self.values['error_name'] = 'That was not a valid name'
        
           
        if have_error:
            self.display_html('med_edit.html')
        else:
            medicine_to_edit.name = name
            medicine_to_edit.directions = directions
            medicine_to_edit.dosage = dosage
            medicine_to_edit.interval = interval 
            
            saved_med = medicine_to_edit.put()
        
            if saved_med:
                self.values['display_message'] = medicine_to_edit.name + " was saved successfully!"
                self.display_html('message.html')
            
            
        
class DeleteMed(Handler):
    def get(self, med_id):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
        
        
        medicine_to_delete = medicines.Medicine().get_medicine_by_key_id(med_id)
        logging.info(medicine_to_delete.key)
        med_key = medicine_to_delete.key
        logging.info(med_key)
        med_key.delete()
        
        self.values['display_message'] = medicine_to_delete.name + " has been deleted!"
        self.display_html('message.html')

        
        
routes = [('/', MainPage),
          ('/signup', SignUp),
          ('/medicines', MedList),
          ('/medicines/new', NewMed),
          (r'/medicines/show/([^/]*)/?$', ShowMed),
          (r'/medicines/([^/]*)/edit/?$', EditMed),
          (r'/medicines/([^/]*)/delete/?$', DeleteMed)
        ]

application = webapp2.WSGIApplication(routes, debug=True)
