# Melon Tasting Reservation Scheduler
### Purpose

I took the take home challenge and it states to build a web application that users can use to search for and book a time slot. They can click the time slot to book. Once they book the time slot, the time slot will appear with "(booked)" as it is not available. They can access their bookings to see the date and the time slot they booked.

## Tech Stack:
### Front-end:
- Bootstrap
- CSS
- HTML
- Javascript
- Jinja2
- JSON
### Back-end:
- API (https://jsonplaceholder.typicode.com/users)
- Flask
- Postgresql
- Python
- SQLAlchemy

## Features

- Front page with Login
![watermelon-1.png](https://www.dropbox.com/s/ng7htpxhcbxneu7/watermelon-1.png?dl=0&raw=1)

- Reservation
![watermelon-2.png](https://www.dropbox.com/s/rodi12rogml7erl/watermelon-2.png?dl=0&raw=1)

- Reservation - Picking a date, start time, and end time
![watermelon-3.png](https://www.dropbox.com/s/20mpd7eig6q11oh/watermelon-3.png?dl=0&raw=1)

- Available Times
![watermelon-4.png](https://www.dropbox.com/s/n7pr2t5rffedjan/watermelon-4.png?dl=0&raw=1)

- Reservation after sucessfully booking time slot
![watermelon-5.png](https://www.dropbox.com/s/49zkcxteh666gc7/watermelon-5.png?dl=0&raw=1)

- Bookings
![watermelon-6.png](https://www.dropbox.com/s/ht52dfm8fn6yvp8/watermelon-6.png?dl=0&raw=1)

- Available Times - With unavailable time slots (booked)
![watermelon-7.png](https://www.dropbox.com/s/mtn0ad6o752im0o/watermelon-7.png?dl=0&raw=1)




## Installation
Clone repository:
```sh
$ git clone https://github.com/lynnec88/melon-booking.git
```
CD to the melon-booking folder
```sh
$ cd melon-booking
```

Create isolated Python environment
```sh
$ virtualenv env
```
```sh
$ source env/bin/activate
```
Install requirements
```sh
$ pip3 install -r requirements.txt
```
Seed databases
```sh
$ python3 seed_database.py
```
Run the app
```sh
$ python3 server.py
```

## TODO✨
- Better styling

- Hiding unavailable times

- Creating a single-page instead of multiple HTML pages

- Deleting or canceling bookings

- Running on  React


## License
Copyright (2023) (Linglin Chen)

All rights reserved.

This copyright notice applies to the contents of the repository hosted on GitHub.com, including but not limited to the source code, documentation, and associated files (collectively referred to as the "Work").

The Work is protected by copyright laws and international treaties. Unauthorized copying, distribution, modification, or use of the Work, in whole or in part, without the explicit permission of the copyright holder is strictly prohibited.

Permission is granted to users to view and download a single copy of the Work for personal, non-commercial use, provided that all copyright notices and other proprietary rights notices are retained.

Any commercial use, reproduction, distribution, or modification of the Work requires prior written permission from the copyright holder.

The Work may contain third-party libraries, tools, or other components that have their own separate licenses and copyright restrictions. Such components are subject to their respective licenses and terms.

The copyright holder disclaims any warranty or liability for the accuracy, completeness, or suitability of the Work and shall not be held responsible for any direct, indirect, incidental, special, or consequential damages arising out of the use or inability to use the Work.

For inquiries regarding the use or licensing of the Work, please contact:

My [LinkedIn]

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   [LinkedIn]: <https://www.linkedin.com/in/linglinchen/>
  