class BellEvent:
    def __init__(self, time, label, event_type):
        self.time = time
        self.label = label
        self.event_type = event_type

    def to_dict(self):
        return {
            "time": self.time,
            "label": self.label,
            "event_type": self.event_type
        }