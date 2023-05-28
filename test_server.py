import unittest
from flask import Flask
from flask_testing import TestCase
from model import User, Booking, connect_to_db, db
from server import app

class ServerTestCase(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        connect_to_db(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_valid_user(self):
        with self.client:
            # create a user and add it to the database
            user = User(username="testuser")
            db.session.add(user)
            db.session.commit()

            # send a POST request to the login route with valid user credentials
            response = self.client.post("/", data={"username": "testuser"}, follow_redirects=True)

            # check if the response contains the expected message
            self.assertIn(b"Logged in.", response.data)

    def test_login_invalid_user(self):
        with self.client:
            # send a POST request to the login route with invalid user credentials
            response = self.client.post("/", data={"username": "invaliduser"}, follow_redirects=True)

            # check if the response contains the expected message
            self.assertIn(b"No such username.", response.data)

    def test_reservation_page_requires_login(self):
        response = self.client.get("/reservation", follow_redirects=True)
        self.assertIn(b"Please log in to access the reservation page.", response.data)

    def test_reservation_page_accessible_after_login(self):
        with self.client:
            # create a user and add it to the database
            user = User(username="testuser")
            db.session.add(user)
            db.session.commit()

            # log in the user
            self.client.post("/", data={"username": "testuser"}, follow_redirects=True)

            # send a GET request to the reservation route
            response = self.client.get("/reservation")

            # check if the response contains the expected content
            self.assertIn(b"Reservation", response.data)

if __name__ == "__main__":
    unittest.main()
