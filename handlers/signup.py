
from models import members
from basehandler import Handler

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
        phonenumber = self.request.get("phonenumber")
        
        
        
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