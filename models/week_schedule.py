from models.day_schedule import DaySchedule


class WeekSchedule:
    def __init__(self, shortened_days=None, shift_mode="single"):
        if shortened_days is None:
            shortened_days = []

        self.shortened_days = shortened_days
        self.shift_mode = shift_mode

        self.days = [
            "Ponedjeljak",
            "Utorak",
            "Srijeda",
            "Četvrtak",
            "Petak"
        ]

    def get_week_schedule(self):
        week_schedule = {}

        for day_name in self.days:
            is_shortened = day_name in self.shortened_days

            day_schedule = DaySchedule(
                day_name=day_name,
                shortened=is_shortened,
                shift_mode=self.shift_mode
            )

            week_schedule[day_name] = day_schedule.get_schedule()

        return week_schedule

    def get_day_schedule(self, day_name):
        is_shortened = day_name in self.shortened_days

        day_schedule = DaySchedule(
            day_name=day_name,
            shortened=is_shortened,
            shift_mode=self.shift_mode
        )

        return day_schedule.get_schedule()

    def get_day_bell_times(self, day_name):
        is_shortened = day_name in self.shortened_days

        day_schedule = DaySchedule(
            day_name=day_name,
            shortened=is_shortened,
            shift_mode=self.shift_mode
        )

        return day_schedule.get_bell_times()