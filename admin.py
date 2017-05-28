from handlers import SendTextMessage
import webapp2

ROUTE_LIST = [
    ('/admin/tasks/sendtextmessage', SendTextMessage)
    ]

APPLICATION = webapp2.WSGIApplication(ROUTE_LIST, debug=True)