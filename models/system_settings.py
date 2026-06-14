class SystemSettings:
    def __init__(self, system_enabled, school_type):
        self.system_enabled = system_enabled
        self.school_type = school_type

    def get_lesson_count(self):
        if self.school_type == "primary":
            return 6
        return 7

    def set_school_type(self, school_type):
        self.school_type = school_type

    def enable_system(self):
        self.system_enabled = True

    def disable_system(self):
        self.system_enabled = False

    def to_dict(self):
        return {
            "system_enabled": self.system_enabled,
            "school_type": self.school_type
        }