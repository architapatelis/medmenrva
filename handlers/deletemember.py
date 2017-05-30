
from models import members
from models import medicines
from handlers import Handler


                


class DeleteMember(Handler):
    def get(self, member_id):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
        
        member_to_delete = members.Member().get_member_by_key_id(member_id)
        member_key = member_to_delete.key
        member_medicine = medicines.Medicine().get_medicines_by_member_key(member_key)
        if member_medicine:
            for medicine in member_medicine:
                med_key = medicine.key
                med_key.delete()
        member_key.delete()
        
        self.display_message(member_to_delete.firstname, " your profile has been deleted successfully!", '/')
        
        
        
        
        
        