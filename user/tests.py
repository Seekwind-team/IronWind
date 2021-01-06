from django.test import TestCase

from user.models import UserData, CompanyData, Authentication
from user.schema import CreateUser

class DemoUser():
    EMAIL = 'demo@must.er'
    PW = '1234'

    def __init__():
        user = CreateUser(user_mutation())

    def user_mutation(self):
        mutation = """
            muatation{
                
            }
        """
    # getter functions
    def mail(self): 
        return EMAIL

    def pw(self): 
        return PW

    def acc(self): 
        return 

class UserTestCase(TestCase):
    def setUp(self):

    def 