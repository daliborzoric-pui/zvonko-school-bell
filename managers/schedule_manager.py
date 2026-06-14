import json


class ScheduleManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_data(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def get_day_settings(self, date_str):
        data = self.load_data()
        return data["days"].get(date_str, {"shortened": False})

    def update_day_settings(self, date_str, shortened):
        data = self.load_data()

        data["days"][date_str] = {
            "shortened": shortened
        }

        self.save_data(data)