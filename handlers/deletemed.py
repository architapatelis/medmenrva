
from models import medicines
from basehandler import Handler



        
class DeleteMed(Handler):
    def get(self, med_id):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
        
        
        medicine_to_delete = medicines.Medicine().get_medicine_by_key_id(med_id)
        med_key = medicine_to_delete.key
        med_key.delete()
        
        self.values['display_message'] = medicine_to_delete.name + " has been deleted!"
        self.display_html('message.html')