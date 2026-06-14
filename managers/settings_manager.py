import json
import os


class SettingsManager:
    def __init__(self, file_path="data/settings.json"):
        self.file_path = file_path

        self.default_settings = {
            "system_enabled": True,
            "school_type": "secondary",
            "shift_mode": "double",
            "shortened_days": []
        }

        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            self.save_settings(self.default_settings)

    def get_settings(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                settings = json.load(file)

            # Ako u settings.json nedostaje neka nova postavka,
            # automatski je dodaj iz default_settings.
            changed = False

            for key, value in self.default_settings.items():
                if key not in settings:
                    settings[key] = value
                    changed = True

            if changed:
                self.save_settings(settings)

            return settings

        except (FileNotFoundError, json.JSONDecodeError):
            self.save_settings(self.default_settings)
            return self.default_settings

    def save_settings(self, settings):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4, ensure_ascii=False)

    def update_setting(self, key, value):
        settings = self.get_settings()
        settings[key] = value
        self.save_settings(settings)