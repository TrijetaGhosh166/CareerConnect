# CareerConnect - Django Job Portal

A full-stack job portal with two roles: Job Seeker and Recruiter.

## Features
- Register and login with role selection (Job Seeker or Recruiter)
- Seeker profile: CGPA, field, skills, experience, resume upload (name, email and mobile are locked)
- Recruiter profile: company, job domain, contact details, Google Form link
- Post jobs, search jobs, read the description, apply
- Application status tracking; recruiters see applicant details and update the status
- Role-based Home page: Profile, Jobs and Application Status sections

## Tech Stack
Python, Django 5, SQLite, Django Templates, Bootstrap 5

## Run Locally
```
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Screenshots
(add images here)

## Future Improvements
Email notifications, password reset, resume validation, pagination, automated tests, REST API

## Author
Trijeta Ghosh - https://github.com/TrijetaGhosh166
