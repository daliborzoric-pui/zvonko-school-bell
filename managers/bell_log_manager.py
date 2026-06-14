import json
from datetime import datetime


class BellLogManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_log(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_log(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_event(self, event_type, label, user="system"):
        data = self.load_log()

        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "label": label,
            "user": user
        }

        data["events"].append(event)
        self.save_log(data)

    def get_events(self):
        data = self.load_log()
        return data["events"]