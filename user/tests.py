from django.test import TestCase
from django.utils import timezone

import graphene

from user.models import UserData, UserManager, CompanyData, Authentication
from user.schema import CreateUser

class DemoUser():
    def __init__(test, is_company):
        self.EMAIL = 'demo@must.er'
        self.PW = '1234'

    
    # builds mutation to create user 
    def create_mutation(self, name = test, is_company=False):
        mutation = """
            mutation {
                createUser(
                    email:"{}@rng.de" 
                    password:"123" 
                    isCompany:{}
                ){
                    user{
                        id
                    }
                }
            }
        """.format(name, is_company)
        return mutation

    # getter functions
    def mail(self): 
        return EMAIL

    def pw(self): 
        return PW

    def acc(self): 
        return user

class UserTestCase(TestCase):
    def setUp(self):
        self.facotry = RequestFactory()
        self.user = UserManager.create_user(email='notarealuseraccount@stupid.gg', password='123')

    def test_details(self):
        query = """
            mutation {
                tokenAuth(
                    email:"notarealuseraccount@stupid.gg"
                    password:"123"
                ){
                    token
                }
            }
        """
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        