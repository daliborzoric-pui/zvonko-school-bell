from datetime import datetime, timedelta


class DaySchedule:
    def __init__(self, day_name, shortened=False, shift_mode="single"):
        self.day_name = day_name
        self.shortened = shortened
        self.shift_mode = shift_mode

        # Početak smjena
        self.first_shift_start = "08:00"
        self.second_shift_start = "14:00"

        # Trajanje sata
        self.normal_lesson_duration = 45
        self.shortened_lesson_duration = 30

        # Odmori
        self.short_break_duration = 5
        self.long_break_duration = 15
        self.entry_after_long_break_delay = 5
        self.long_break_after_lesson = 2

        # Default broj sati.
        # app.py kasnije postavlja 6 za osnovnu ili 7 za srednju školu.
        self.lesson_count = 6

    def _string_to_time(self, time_string):
        return datetime.strptime(time_string, "%H:%M")

    def _time_to_string(self, time_value):
        return time_value.strftime("%H:%M")

    def _get_lesson_duration(self):
        if self.shortened:
            return self.shortened_lesson_duration

        return self.normal_lesson_duration

    def _generate_shift_schedule(self, shift_name, start_time):
        current_time = self._string_to_time(start_time)
        lesson_duration = self._get_lesson_duration()

        lessons = []

        for lesson_number in range(1, self.lesson_count + 1):
            lesson_start = current_time
            lesson_end = lesson_start + timedelta(minutes=lesson_duration)

            lessons.append({
                "shift": shift_name,
                "lesson_number": lesson_number,
                "label": f"{lesson_number}. sat",
                "start": self._time_to_string(lesson_start),
                "end": self._time_to_string(lesson_end)
            })

            current_time = lesson_end

            if lesson_number < self.lesson_count:
                if lesson_number == self.long_break_after_lesson:
                    # Veliki odmor, npr. 09:35 - 09:50
                    current_time += timedelta(minutes=self.long_break_duration)

                    # Zvono za ulazak je nakon velikog odmora,
                    # a početak sljedećeg sata je 5 minuta kasnije.
                    current_time += timedelta(minutes=self.entry_after_long_break_delay)
                else:
                    # Mali odmor između ostalih sati
                    current_time += timedelta(minutes=self.short_break_duration)

        return lessons

    def get_schedule(self):
        schedule = {
            "first_shift": self._generate_shift_schedule(
                shift_name="first",
                start_time=self.first_shift_start
            )
        }

        if self.shift_mode == "double":
            schedule["second_shift"] = self._generate_shift_schedule(
                shift_name="second",
                start_time=self.second_shift_start
            )

        return schedule

    def get_bell_times(self):
        schedule = self.get_schedule()
        bell_times = []

        for shift_lessons in schedule.values():
            for lesson in shift_lessons:
                bell_times.append({
                    "shift": lesson["shift"],
                    "lesson_number": lesson["lesson_number"],
                    "time": lesson["start"],
                    "type": "start"
                })

                bell_times.append({
                    "shift": lesson["shift"],
                    "lesson_number": lesson["lesson_number"],
                    "time": lesson["end"],
                    "type": "end"
                })

                # Posebno zvono za ulazak nakon velikog odmora
                if lesson["lesson_number"] == self.long_break_after_lesson:
                    lesson_end_time = self._string_to_time(lesson["end"])

                    entry_time = lesson_end_time + timedelta(
                        minutes=self.long_break_duration
                    )

                    bell_times.append({
                        "shift": lesson["shift"],
                        "lesson_number": lesson["lesson_number"] + 1,
                        "time": self._time_to_string(entry_time),
                        "type": "entry_after_long_break"
                    })

        bell_times.sort(key=lambda item: item["time"])

        return bell_times