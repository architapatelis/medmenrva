from google.appengine.ext import ndb

class Medicine(ndb.Model):
    name = ndb.StringProperty()
    directions = ndb.StringProperty()
    dosage = ndb.StringProperty()
    interval = ndb.IntegerProperty()
    quantity = ndb.IntegerProperty()
    date_and_time = ndb.DateTimeProperty()
    member = ndb.KeyProperty()
    
    @staticmethod
    def get_medicines_by_member_key(member):
        return Medicine.query(Medicine.member==member).fetch()