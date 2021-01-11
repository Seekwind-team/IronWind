from django.test import TestCase, RequestFactory
from django.utils import timezone

from graphene_django.utils.testing import GraphQLTestCase
import graphene
import json

from user.models import UserData, UserManager, CompanyData, Authentication
from user.schema import CreateUser

class MyFancyTestCase(GraphQLTestCase):
    def test_some_query(self):
        response = self.query(
            '''
            {
                ping
            }
            '''
        )

        # This validates the status code and if you get errors
        try:
            content = json.loads(response.content)
            self.assertResponseNoErrors(response)
        except:
            print(response.content)


"""
    def test_details(self):
        query = "
            mutation {
                tokenAuth(
                    email:"notarealuseraccount@stupid.gg"
                    password:"123"
                ){
                    token
                }
            }
        "
        schema = graphene.Schema(query=Query)
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        
# creates a DemoUser Object. Adding User to DB and storing User-Information
class DemoUser(email = "demo@us.er", password = "123"):
    def __init__(self, email = "demo@us.er", password = "123"):
        self.email = email
        self.password = password

        # Create User mutation
        payload_create_user = "
        mutation {
            createUser(
                email:"%s"
                isCompany:true
                password:"%s"
            ){
                user{id}
            }
        }
        " %(email, password)

        self.user = helper.run_payload(helper, payload = payload_create_user)

"""