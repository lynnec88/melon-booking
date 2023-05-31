from flask import Flask, render_template, redirect, flash, session, request
from datetime import datetime, timedelta
from model import User, Booking, connect_to_db, db
import os
import crud

app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.secret_key = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql://melonbooking_user:bAkmE8vhyNA1D2vnWY4PwWeNIgDMdD5Z@dpg-chrqer1mbg582kdmgq40-a.oregon-postgres.render.com/melonbooking"
)
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
                user = crud.get_by_username(username)
                if user is None:
                    flash("User not found.")
                    return redirect("/")

                booking = crud.create_booking(user.user_id, date, time)
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
        user = crud.get_by_username(username)
        if user is None:
            flash("User not found.")
            return redirect("/")

        appointments = crud.get_user_bookings(user.user_id)

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

        if date and start_time and end_time:
            if is_time_slot_available(date, start_time, end_time):
                flash("The selected time slot is available.")
            else:
                flash("The selected time slot is already booked. Please choose another time.")
        else:
            flash("Invalid request. Please provide a date, start time, and end time.")

        return redirect("/reservation")
    else:
        flash("Please log in to access the reservation page.")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
