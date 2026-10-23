from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, display_name, avatar_url=None):
        self.id = id
        self.email = email
        self.display_name = display_name
        self.avatar_url = avatar_url