class Lesson:
    def __init__(self, lesson_number, start_time, end_time, duration):
        self.lesson_number = lesson_number
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration

    def to_dict(self):
        return {
            "lesson_number": self.lesson_number,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration
        }