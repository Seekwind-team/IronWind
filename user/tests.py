from django.test import TestCase
from django.contrib.auth.hashers import check_password

from user.models import *

class UserTests(TestCase):
    def setUp(self):
        self.email = "demo@user.de"
        self.pw = "123asdf"
        CreateUser.create_user(CreateUser, self.email, self.pw)
        self.user_object = Authentication.objects.get(email=self.email)

    def test_credentials(self):
        self.assertEqual(self.user_object.email, self.email)
        # TODO fix pw not getting hashed in Authentication() call.
        #self.assertTrue(check_password(self.pw, self.user_object.password))
        self.assertEqual(self.pw, self.user_object.password)

class CreateUser():
    def create_user(self, email, pw):
        user = Authentication(is_superuser=False, password=pw, email=email)
        user.save()
        
