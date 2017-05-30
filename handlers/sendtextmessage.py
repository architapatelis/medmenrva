from basehandler import Handler
from models import Medicine
import arrow
import logging
from api import twilio_utils

class SendTextMessage(Handler):
    def get(self):
        self.text_message_task()
        
    def text_message_task(self):
        logging.info("executing send text message method")
        list_of_medicines_to_text = Medicine().get_medicine_by_text_time()
        for medicine in list_of_medicines_to_text:
            if medicine.quantity > 0:
                new_text_time = arrow.get(medicine.date_and_time).replace(hours=+medicine.interval)
                medicine.date_and_time = new_text_time.naive
                medicine.quantity -= medicine.dosage
                medicine.put()
                member = medicine.member.get()
                twilio_utils.send_text_message(medicine.name, medicine.dosage, member.phonenumber, medicine.directions)
                