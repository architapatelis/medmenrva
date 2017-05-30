
from models import members
from basehandler import Handler


                
class EditMember(Handler):
    def get(self, member_id):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
        
        member_to_edit = members.Member().get_member_by_key_id(member_id)
        self.values["member_to_edit"] = member_to_edit
        
        self.display_html('edit_member.html')
    
    def post(self, member_id):  
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url(False))
            
        
        member_to_edit = members.Member().get_member_by_key_id(member_id)
        self.values["member_to_edit"] = member_to_edit
    
        firstname = self.request.get('firstname')
        lastname = self.request.get('lastname')
        phonenumber = self.request.get('phonenumber')
        
        
        have_error = False
        valid_firstname = self.valid_name(firstname)
        valid_lastname = self.valid_name(lastname)
        valid_phonenumber = self.valid_phonenumber(phonenumber)
        
        if not valid_firstname:
            have_error = True
            self.values['error_firstname'] = 'This is not a valid firstname'
        if not valid_lastname:
            have_error = True
            self.values['error_lastname'] = 'This is not a valid lastname'
        if not valid_phonenumber:
            have_error = True
            self.values['error_phonenumber'] = 'This is not a valid phonenumber'
        
           
        if have_error:
            self.display_html('edit_member.html')
        else:
            member_to_edit.firstname = firstname
            member_to_edit.lastname = lastname
            member_to_edit.phonenumber = phonenumber
            
            saved_member = member_to_edit.put()
        
            if saved_member:
                self.values['display_message'] = member_to_edit.firstname + " your profile has been edited successfully!"
                self.display_html('message.html')

