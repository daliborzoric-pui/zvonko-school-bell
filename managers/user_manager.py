import json
from models.user import User


class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_users(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        users = []
        for item in data:
            user = User(
                item["username"],
                item["password"],
                item["first_name"],
                item["last_name"]
            )
            users.append(user)

        return users

    def find_user_by_username(self, username):
        users = self.load_users()

        for user in users:
            if user.username == username:
                return user

        return None