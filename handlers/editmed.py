
from models import medicines
from basehandler import Handler

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
                self.values['display_message'] = medicine_to_edit.name + " was edited successfully!"
                self.display_html('message.html')
            