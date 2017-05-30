import webapp2
from handlers import MainPage
from handlers import SignUp
from handlers import MedList
from handlers import NewMed
from handlers import ShowMed
from handlers import EditMed
from handlers import DeleteMed
from handlers import EditMember
from handlers import DeleteMember

        
routes = [('/', MainPage),
          ('/signup', SignUp),
          ('/medicines', MedList),
          ('/medicines/new', NewMed),
          (r'/medicines/show/([^/]*)/?$', ShowMed),
          (r'/medicines/([^/]*)/edit/?$', EditMed),
          (r'/medicines/([^/]*)/delete/?$', DeleteMed),
          (r'/members/([^/]*)/edit/?$', EditMember),
          (r'/members/([^/]*)/delete/?$', DeleteMember)
        ]

application = webapp2.WSGIApplication(routes, debug=True)
