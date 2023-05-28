from model import db, User, Booking, connect_to_db


def create_user(username):
    """ Create and return a user """

    user = User(username=username)

    return user


def get_by_username(username):
    """ Return user by username"""

    user = User.query.filter(User.username == username).first()

    return user


def get_user_id_by_username(username):
    """ Return user id by username"""

    user = User.query.filter(User.username == username).first()

    return user.user_id


def create_booking(user_id, date_str, time):
    """ Create a booking for tasting melons """

    booking = Booking(user_id=user_id, date_str=date_str, time=time)

    return booking



def get_user_bookings(user_id):
    """ Return user bookings """

    bookings = Booking.query.filter_by(user_id=user_id).all()

    return bookings


def get_all_bookings_by_date(date_str):
    """ Return all bookings by date """

    all_bookings = Booking.query.filter_by(date_str=date_str).all()

    return all_bookings
