
from models import medicines
from handlers import Handler



class MedList(Handler):
    def get(self):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
        
        list_of_medicines = medicines.Medicine().get_medicines_by_member_key(self.member.key)
        self.values['medicines'] = list_of_medicines
        self.display_html('med_index.html')