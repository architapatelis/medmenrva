from google.appengine.ext import ndb

class Member(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    phonenumber = ndb.StringProperty()
    email = ndb.StringProperty()
    
    @staticmethod
    def check_is_member(email):
        member = Member.query(Member.email==email).get()
        if member:
            return True
        else:
            return False
        