
from models import medicines
import arrow
from basehandler import Handler



    
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
            medicine.timezone = timezone
            medicine.member = member
            
            
            saved_med = medicine.put()
            
            
            if saved_med:
                self.values['display_message'] = medicine.name + " was saved successfully!"
                self.display_html('message.html')