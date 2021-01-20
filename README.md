# IronWind
Backend section for WhiteWater

#Getting Started
### Getting Started KI (Tensorflow):

- Python 3.8.6 installieren https://www.python.org/downloads/release/python-386/
- tensorflow-gpu 2.3.x installieren https://www.tensorflow.org/install/pip

### Getting Started Controller/DB

required imports (pip):
```py
$ pip install -U pip Django django-graphql-jwt graphene-django graphene-file-upload channels_redis graphene-subscriptions
```
starting the server:
execute the following commands in this directory
```py
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

### running the SQLite Database/Dev environment locally
If you are running the Dev environment on Windows you will be most like to run into this Error 
```SystemCheckError: System check identified some issues:
ERRORS:
user.UserData: (fields.E180) SQLite does not support JSONFields.
```

To remedy this issue you will need the steps provided in https://code.djangoproject.com/wiki/JSON1Extension.

Should you be on Mac or Linux, this most likely won't apply to you, so you can ignore this step. 

## Structure
```py
IronWind/
├─ recommenders/ # Folder for connecting the ML-Framework
├─ static/ # Folder for static files (eg. HTML, CSS)
├─ user/
│  ├─ migrations/ # folder that holds all informatiion colected by ORM
│  ├─ admin.py # file for referencing data models in admin view
│  ├─ apps.py  # app config
│  ├─ models.py # File responsible for the generation of Database Objects via ORM
│  ├─ schema.py # API-Controller 
│  ├─ tests.py # file for automated testing of this section
│  ├─ views.py # unused here
├─ joboffer/
│  ├─ migrations/ # folder that holds all informatiion colected by ORM
│  ├─ admin.py # file for referencing data models in admin view
│  ├─ apps.py # app config
│  ├─ models.py # File responsible for the generation of Database Objects via ORM
│  ├─ schema.py # API-Controller 
│  ├─ tests.py # file for automated testing of this section
│  ├─ views.py # unused here
├─ chat/
│  ├─ migrations/ # folder that holds all informatiion colected by ORM
│  ├─ admin.py # file for referencing data models in admin view
│  ├─ apps.py # app config
│  ├─ models.py # File responsible for the generation of Database Objects via ORM
│  ├─ schema.py # API-Controller 
│  ├─ signals.py
│  ├─ tests.py # file for automated testing of this section
│  ├─ views.py # unused here
├─ carespace/
│  ├─ migrations/ # folder that holds all informatiion colected by ORM
│  ├─ admin.py # file for referencing data models in admin view
│  ├─ apps.py # app config
│  ├─ models.py # File responsible for the generation of Database Objects via ORM
│  ├─ schema.py # API-Controller 
│  ├─ tests.py # file for automated testing of this section
│  ├─ views.py # unused here
├─ IronWind/
│  ├─ asgi.py # definition file for asgi application
│  ├─ routing.py # file for defining web sockets
│  ├─ schema.py # root file for API-Controller 
│  ├─ settings.py # project settings file
│  ├─ urls.py # file for defining all (HTTP-) URL-Routes
│  ├─ wsgi.py # definition file for wsgi application
├─ tests/
│  ├─ helper.py # Helper functions
│  ├─ int_*.py # integrationtest. * defines what will be tested (eg. ironwind-api)
│  ├─ mod_*.py # moduletest. * defines what will be tested (eg. ironwind-user)
```


## Abgabeumfang

Im Abgabeumfang an den Kunden sind alle Dateien außer
- `test`-Ordner
- `static`-Ordner
- `.github`-Ordner
- `.gitignore`-Datei

enthalten.
