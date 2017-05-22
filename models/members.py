from google.appengine.ext import ndb

class Member(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    phonenumber = ndb.StringProperty()
    email = ndb.StringProperty()
    
    @staticmethod
    def get_member_by_email(email):
        return Member.query(Member.email==email).get()
        
    
    