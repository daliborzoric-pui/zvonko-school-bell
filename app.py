from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta

from managers.settings_manager import SettingsManager
from managers.schedule_manager import ScheduleManager
from managers.bell_log_manager import BellLogManager
from models.day_schedule import DaySchedule


app = Flask(__name__)
app.secret_key = "moja_tajna_lozinka_123"

# Jedini korisnik sustava
USERNAME = "admin"
PASSWORD = "Skzvono.26"
FULL_NAME = "Administrator"

settings_manager = SettingsManager("data/settings.json")
schedule_manager = ScheduleManager("data/schedule.json")
bell_log_manager = BellLogManager("data/bell_log.json")

# Globalno stanje zvona u memoriji aplikacije
bell_state = {
    "active_until": None,
    "last_manual_trigger": None,
    "last_auto_trigger_key": None,
    "sound_token": 0
}


DAY_NAMES = [
    "Ponedjeljak",
    "Utorak",
    "Srijeda",
    "Četvrtak",
    "Petak",
    "Subota",
    "Nedjelja"
]


def activate_bell():
    """Aktivira zvono na 5 sekundi."""
    bell_state["active_until"] = datetime.now() + timedelta(seconds=5)
    bell_state["sound_token"] += 1


def is_bell_active():
    """Provjerava je li zvono trenutno aktivno."""
    active_until = bell_state["active_until"]

    if active_until is None:
        return False

    return datetime.now() < active_until


def load_settings():
    """
    Učitava postavke aplikacije.
    Ako neke postavke nedostaju, dodaju se automatski.
    """
    settings = settings_manager.get_settings()

    if "system_enabled" not in settings:
        settings["system_enabled"] = True

    if "school_type" not in settings:
        settings["school_type"] = "secondary"

    if "shift_mode" not in settings:
        settings["shift_mode"] = "single"

    if "shortened_days" not in settings:
        settings["shortened_days"] = []

    settings_manager.save_settings(settings)

    return settings


def get_lesson_count(settings):
    """
    Vraća broj školskih sati prema tipu škole.

    Osnovna škola ima 6 sati.
    Srednja škola ima 7 sati.
    """
    school_type = settings.get("school_type", "primary")

    if school_type == "secondary":
        return 7

    return 6


def get_week_start(date_value):
    """Vraća ponedjeljak za odabrani tjedan."""
    return date_value - timedelta(days=date_value.weekday())


def get_week_days(week_date, selected_date):
    """Kreira listu dana za prikaz tjednog rasporeda."""
    week_start = get_week_start(week_date)
    week_days = []

    for i in range(5):
        current_date = week_start + timedelta(days=i)

        week_days.append({
            "name": DAY_NAMES[current_date.weekday()],
            "date": current_date,
            "date_iso": current_date.strftime("%Y-%m-%d"),
            "display": current_date.strftime("%d.%m.%Y."),
            "is_selected": selected_date == current_date
        })

    return week_days


def build_day_schedule_for_date(target_date, settings):
    """Gradi raspored za konkretan datum."""
    date_iso = target_date.strftime("%Y-%m-%d")
    day_name = DAY_NAMES[target_date.weekday()]

    day_settings = schedule_manager.get_day_settings(date_iso)
    shortened = day_settings.get("shortened", False)

    shift_mode = settings.get("shift_mode", "single")
    lesson_count = get_lesson_count(settings)

    day_schedule = DaySchedule(
        day_name=day_name,
        shortened=shortened,
        shift_mode=shift_mode
    )

    day_schedule.lesson_count = lesson_count

    return day_schedule


def flatten_lessons(schedule):
    """
    Pretvara raspored smjena u jednu listu lekcija za HTML prikaz.
    """
    lessons = []

    if "first_shift" in schedule:
        lessons.extend(schedule["first_shift"])

    if "second_shift" in schedule:
        lessons.extend(schedule["second_shift"])

    return lessons


def build_bell_event_label(event):
    """Kreira čitljiv naziv događaja zvonjenja."""
    shift_label = "1. smjena" if event["shift"] == "first" else "2. smjena"

    if event["type"] == "start":
        return f"{shift_label} - početak {event['lesson_number']}. sata"

    if event["type"] == "end":
        return f"{shift_label} - kraj {event['lesson_number']}. sata"

    if event["type"] == "entry_after_long_break":
        return f"{shift_label} - ulazak nakon velikog odmora"

    return f"{shift_label} - zvonjenje"


def check_automatic_bell():
    """Provjera treba li automatski uključiti zvono po rasporedu."""
    settings = load_settings()

    if not settings.get("system_enabled", True):
        return

    now = datetime.now()
    today = now.date()

    # Vikendom nema automatskog zvonjenja
    if today.weekday() >= 5:
        return

    current_time_str = now.strftime("%H:%M")
    today_key = today.strftime("%Y-%m-%d")

    day_schedule = build_day_schedule_for_date(today, settings)
    bell_events = day_schedule.get_bell_times()

    for event in bell_events:
        if event["time"] == current_time_str:
            trigger_key = (
                f"{today_key}_"
                f"{event['shift']}_"
                f"{event['lesson_number']}_"
                f"{event['time']}_"
                f"{event['type']}"
            )

            # Sprječava višestruko okidanje unutar iste minute
            if bell_state["last_auto_trigger_key"] != trigger_key:
                activate_bell()

                bell_log_manager.add_event(
                    event_type="automatic",
                    label=build_bell_event_label(event),
                    user="Sustav"
                )

                bell_state["last_auto_trigger_key"] = trigger_key

            return


@app.route("/", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["username"] = USERNAME
            session["full_name"] = FULL_NAME
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Pogrešno korisničko ime ili lozinka."
        )

    return render_template("login.html", error=None)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    settings = load_settings()

    week_date_str = request.args.get("week_date")
    selected_date_str = request.args.get("selected_date")

    today = datetime.today().date()

    if week_date_str:
        week_date = datetime.strptime(week_date_str, "%Y-%m-%d").date()
    else:
        week_date = today

    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    else:
        if not week_date_str and today.weekday() < 5:
            selected_date = today
        else:
            selected_date = None

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "system_settings":
            school_type = request.form.get("school_type", "secondary")
            shift_mode = request.form.get("shift_mode", "single")
            system_enabled_value = request.form.get("system_enabled")

            settings["school_type"] = school_type
            settings["shift_mode"] = shift_mode
            settings["system_enabled"] = system_enabled_value == "on"

            settings_manager.save_settings(settings)

        elif form_type == "day_settings" and selected_date is not None:
            selected_date_iso = selected_date.strftime("%Y-%m-%d")
            shortened_value = request.form.get("shortened")
            shortened = shortened_value == "on"

            schedule_manager.update_day_settings(
                selected_date_iso,
                shortened
            )

        redirect_args = {
            "week_date": week_date.strftime("%Y-%m-%d")
        }

        if selected_date is not None:
            redirect_args["selected_date"] = selected_date.strftime("%Y-%m-%d")

        return redirect(url_for("dashboard", **redirect_args))

    week_days = get_week_days(week_date, selected_date)

    for day in week_days:
        day_iso = day["date"].strftime("%Y-%m-%d")
        day_data = schedule_manager.get_day_settings(day_iso)
        day["is_shortened"] = day_data.get("shortened", False)

    previous_week_date = (
        get_week_start(week_date) - timedelta(days=7)
    ).strftime("%Y-%m-%d")

    next_week_date = (
        get_week_start(week_date) + timedelta(days=7)
    ).strftime("%Y-%m-%d")

    if selected_date is not None:
        selected_date_iso = selected_date.strftime("%Y-%m-%d")
        selected_date_display = selected_date.strftime("%d.%m.%Y.")

        day_settings = schedule_manager.get_day_settings(selected_date_iso)

        day_schedule = build_day_schedule_for_date(
            selected_date,
            settings
        )

        schedule = day_schedule.get_schedule()
        lessons = flatten_lessons(schedule)

        bell_events = day_schedule.get_bell_times()

        for event in bell_events:
            event["label"] = build_bell_event_label(event)

    else:
        selected_date_iso = None
        selected_date_display = "Nije odabran dan"
        day_settings = {"shortened": False}
        lessons = []
        bell_events = []

    return render_template(
        "dashboard.html",
        full_name=session["full_name"],
        settings=settings,
        lesson_count=get_lesson_count(settings),
        week_days=week_days,
        selected_date=selected_date_display,
        selected_date_iso=selected_date_iso,
        previous_week_date=previous_week_date,
        next_week_date=next_week_date,
        current_week_date=week_date.strftime("%Y-%m-%d"),
        day_settings=day_settings,
        lessons=lessons,
        bell_events=bell_events
    )


@app.route("/ring_bell", methods=["POST"])
def ring_bell():
    if "username" not in session:
        return jsonify({"status": "unauthorized"}), 401

    settings = load_settings()

    if not settings.get("system_enabled", True):
        return jsonify({"status": "disabled"}), 403

    activate_bell()

    bell_log_manager.add_event(
        event_type="manual",
        label="Ručno zvonjenje",
        user=session["full_name"]
    )

    bell_state["last_manual_trigger"] = datetime.now().isoformat()

    return jsonify({"status": "ok"})


@app.route("/bell_status")
def bell_status():
    if "username" not in session:
        return jsonify({
            "active": False,
            "sound_token": bell_state["sound_token"]
        })

    check_automatic_bell()

    return jsonify({
        "active": is_bell_active(),
        "sound_token": bell_state["sound_token"]
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)