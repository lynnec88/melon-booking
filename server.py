from flask import Flask, render_template, redirect, flash, session, request
from datetime import datetime, timedelta
from model import User, Booking, connect_to_db, db
import os
import crud

app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.secret_key = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgres://melonbooking_user:bAkmE8vhyNA1D2vnWY4PwWeNIgDMdD5Z@dpg-chrqer1mbg582kdmgq40-a/melonbooking")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
connect_to_db(app)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get('username')
        user = crud.get_by_username(username)
        if not user:
            flash("No such username.")
            return redirect('/')
        session["logged_in_username"] = user.username
        flash("Logged in.")
        return redirect("/reservation")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("logged_in_username", None)
    flash("Logged out successfully.")
    return redirect("/")

@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    if "logged_in_username" in session:
        if request.method == "POST":
            date = request.form.get('date')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            time = f"{start_time} - {end_time}"

            if is_time_slot_available(date, start_time, end_time):
                username = session["logged_in_username"]
                user = User.query.filter_by(username=username).first()
                if user is None:
                    flash("User not found.")
                    return redirect("/")

                booking = Booking(
                    user_id=user.user_id,
                    date_str=date,
                    time=time,
                    start_time_str=start_time,
                    end_time_str=end_time
                )
                db.session.add(booking)
                db.session.commit()

                flash("Reservation successful!")
                return redirect("/reservation-success")
            else:
                flash("The selected time slot is already booked. Please choose another time.")
                return redirect("/reservation")
        else:
            book = "Some value"
            date = "Some value"
            start_time = "Some value"
            end_time = "Some value"

            return render_template("reservation.html", book=book, date=date, start_time=start_time, end_time=end_time)
    else:
        flash("Please log in to access the reservation page.")
        return redirect("/")

@app.route("/scheduled-appointments", methods=["GET"])
def scheduled_appointments():
    if "logged_in_username" in session:
        username = session["logged_in_username"]
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("User not found.")
            return redirect("/")

        appointments = Booking.query.filter_by(user_id=user.user_id).all()

        return render_template("scheduled_appointments.html", appointments=appointments)
    else:
        flash("Please log in to access the reservation page.")
        return redirect("/")

@app.route("/availability", methods=["GET"])
def check_availability():
    if "logged_in_username" in session:
        date = request.args.get("date")
        start_time = request.args.get("start_time")
        end_time = request.args.get("end_time")

        available_times = generate_available_times(date, start_time, end_time)
        unavailable_times = get_unavailable_times(date, start_time, end_time)

        return render_template("availability.html", available_times=available_times, date=date, start_time=start_time, end_time=end_time, unavailable_times=unavailable_times)
    else:
        flash("Please log in to access the reservation page.")
        return redirect("/")

def get_unavailable_times(date, start_time, end_time):
    # retrieve the booked times from the database for the specified date and time range.
    bookings = Booking.query.filter(
        Booking.date_str == date,
        Booking.time >= start_time,
        Booking.time <= end_time
    ).all()

    # extract the booked times from the bookings.
    booked_times = [booking.time for booking in bookings]

    # generate a list of all possible times within the specified range.
    selected_start_time = datetime.strptime(start_time, "%H:%M")
    selected_end_time = datetime.strptime(end_time, "%H:%M")
    time_increment = timedelta(minutes=30)

    current_time = selected_start_time
    all_times = []
    while current_time <= selected_end_time:
        all_times.append(current_time.strftime("%H:%M"))
        current_time += time_increment

    # filter out the booked times from all possible times to get the unavailable times.
    unavailable_times = [time for time in all_times if time in booked_times]

    return unavailable_times

@app.route("/reservations/book", methods=["GET"])
def book_reservation():
    if "logged_in_username" in session:
        time = request.args.get("time")
        date = request.args.get("date")

        booking = Booking.query.filter_by(date_str=date, time=time).first()
        if booking is not None:
            flash("The selected time slot is already booked. Please choose another time.")
            return redirect("/availability")

        username = session["logged_in_username"]
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("User not found.")
            return redirect("/")

        booking = Booking(date_str=date, time=time, user=user)
        db.session.add(booking)
        db.session.commit()

        flash("Reservation for {} on {} booked successfully!".format(time, date))
        return redirect("/reservation")
    else:
        flash("Please log in to access the reservation page.")
        return redirect("/")

def generate_available_times(date, start_time, end_time):
    selected_date = datetime.strptime(date, "%Y-%m-%d")
    selected_start_time = datetime.strptime(start_time, "%H:%M")
    selected_end_time = datetime.strptime(end_time, "%H:%M")

    duration = selected_end_time - selected_start_time
    num_intervals = int(duration.total_seconds() / (30 * 60))

    available_times = []
    current_time = selected_start_time

    for _ in range(num_intervals):
        available_times.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)

    return available_times

def is_time_slot_available(date, start_time, end_time):
    booking = Booking.query.filter(
        Booking.date_str == date,
        Booking.start_time_str <= start_time,
        Booking.end_time_str >= end_time
    ).first()
    return booking is None

if __name__ == "__main__":
    app.run(debug=True)
