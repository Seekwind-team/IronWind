**setup and run Django tests**
# running tests from the tests dir does not work. Tests are saved in each directory in a tests.py. (eg. IronWind/users/tests.py for all User-Object tests)
# to run all tests simply
python manage.py test

# to run a specific test
python manage.py test relative/path
# eg. (only run tests for JobOffers):
python manage.py test joboffer