# CareerConnect - basic Django job portal

## Run
```
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations accounts jobs applications
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```
If you ran an earlier version, delete db.sqlite3 and the migrations folders first.
