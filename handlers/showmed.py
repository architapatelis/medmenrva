
from models import medicines
import arrow
from handlers import Handler


class ShowMed(Handler):
    def get(self, med_id):
        if not self.is_user_signed_up():
            return self.redirect(self.make_login_url())
    
        medicine_to_show = medicines.Medicine().get_medicine_by_key_id(med_id)
        
        self.values['medicine_to_show'] = medicine_to_show
        local_date_and_time = arrow.get(medicine_to_show.date_and_time).to(medicine_to_show.timezone)
        next_dosage_date_and_time = local_date_and_time.naive
        next_dosage_date = next_dosage_date_and_time.strftime("%B %d, %Y")
        next_dosage_time = next_dosage_date_and_time.strftime("%I:%M%p")
        self.values['next_dosage_date'] = next_dosage_date
        self.values['next_dosage_time'] = next_dosage_time
        self.display_html('med_show.html')