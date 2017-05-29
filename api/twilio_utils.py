from twilio.rest import Client
import os

# Find these values at https://twilio.com/user/account
account_sid = os.environ.get('TWILIO_SID', '')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
twilio_number = os.environ.get('TWILIO_NUMBER', '')

client = Client(account_sid, auth_token)

def send_text_message(name, dosage, phonenumber, directions=None):
    message = "Take %s pill of %s." % (dosage, name)
    if directions:
        message += " Directions: %s" % directions
    
        
    
    text_message = client.api.account.messages.create(to=phonenumber,
                                                      from_=twilio_number,
                                                      body=message)
    
    return text_message