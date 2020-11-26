# IronWind
Backend section for WhiteWater

## Getting Started KI (Tensorflow):

- Python 3.8.6 installieren https://www.python.org/downloads/release/python-386/
- tensorflow-gpu 2.3.x installieren https://www.tensorflow.org/install/pip

## Getting Started Controller/DB

required imports (pip):
```py
$ pip install -U pip Django django-graphql-jwt graphene-django graphene-file-upload 
```
getting started:
```py
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
