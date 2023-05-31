from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'


class Booking(db.Model):
    """Booking model"""

    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_str = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)

    user = db.relationship('User', backref='bookings')

    def __repr__(self):
        return f'<Booking booking_id={self.booking_id} user_id={self.user_id} date_str={self.date_str} time={self.time}>'


def connect_to_db(app):
    """Connect the database to Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://melonbooking_user:bAkmE8vhyNA1D2vnWY4PwWeNIgDMdD5Z@dpg-chrqer1mbg582kdmgq40-a.oregon-postgres.render.com/melonbooking'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

print("Connected to the database!")
