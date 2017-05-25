from google.appengine.ext import ndb

class Medicine(ndb.Model):
    name = ndb.StringProperty()
    directions = ndb.StringProperty()
    dosage = ndb.IntegerProperty()
    interval = ndb.IntegerProperty()
    quantity = ndb.IntegerProperty()
    date_and_time = ndb.DateTimeProperty()
    member = ndb.KeyProperty()
    
    
    @staticmethod
    def get_medicines_by_member_key(member_key):
        return Medicine.query(Medicine.member==member_key).fetch()
    
    @staticmethod
    def get_medicine_by_key_id(key_id):
        med = None
        try:
            med = ndb.Key(urlsafe=key_id).get()
        except:
            med = None
        return med
    
    
    
    
    
    
