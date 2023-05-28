import os
import requests
from datetime import date

from model import db, User, Booking, connect_to_db
import server
import crud

os.system("dropdb melonbooking")
os.system("createdb melonbooking")

# create the database tables
db.create_all()

# fetch user data from API
response = requests.get('https://jsonplaceholder.typicode.com/users')
user_data = response.json()

users_in_db = []
for user in user_data:
    username = user['username']

    new_user = crud.create_user(username)
    db.session.add(new_user)
    db.session.commit()

    user_id = crud.get_user_id_by_username(username)
    # date_str = str(date.today())
    # time = ''
    # booking = crud.create_booking(user_id, date_str, time)
    # db.session.add(booking)
    # db.session.commit()
