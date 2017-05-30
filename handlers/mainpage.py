
from basehandler import Handler


class MainPage(Handler):
    def get(self):
        self.add_member_key_to_values_dict()
        self.display_html("home.html")