from model import db, User, Booking


def create_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return user


def get_by_username(username):
    user = User.query.filter(User.username == username).first()
    return user


def get_user_id_by_username(username):
    user = User.query.filter(User.username == username).first()
    return user.user_id


def create_booking(user_id, date_str, time):
    booking = Booking(user_id=user_id, date_str=date_str, time=time)
    db.session.add(booking)
    db.session.commit()
    return booking


def get_user_bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return bookings


def get_all_bookings_by_date(date_str):
    all_bookings = Booking.query.filter_by(date_str=date_str).all()
    return all_bookings
