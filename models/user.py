class User:
    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password):
        return self.password == password

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"