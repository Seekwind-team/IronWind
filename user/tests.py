from django.test import TestCase

from user.models import *

class UserTests(TestCase):
    def setUp(self):
        self.email = "demo@user.de"
        self.pw = "123asdf"
        self.create_user(self.email, self.pw)

    def test_credentials(self):
        user_object = Authentication.objects.get(email=self.email)
        if user_object != None:
            print(user_object)
        else:
            print("lkashdöoifaäweibväoaivebäpaespaoskjlfjasd")
            
    def create_user(self, email, pw):
        #if email in Authentication.objects.raw('SELECT email FROM user_authentication'):
        #    raise Error('email already in use')
            
        Authentication.objects.raw('''
            INSERT into user_authentication (password, email) 
            VALUES ('{password}', '{email}')
        '''.format(password = pw, email = email))
        
        return True

''' python manage.py dbshell && .tables
auth_group                            joboffer_joboffer                   
auth_group_permissions                joboffer_joboffer_hashtags          
auth_permission                       joboffer_swipe                      
carespace_carespace                   joboffer_tag                        
chat_message                          user_authentication                 
django_admin_log                      user_authentication_groups          
django_content_type                   user_authentication_user_permissions
django_migrations                     user_companydata                    
django_session                        user_note                           
joboffer_bookmark                     user_softskills                     
joboffer_image                        user_userdata     

sqlite> select sql from sqlite_master where name='user_authentication';
CREATE TABLE "user_authentication" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "password" varchar(128) NOT NULL, 
    "last_login" datetime NULL, 
    "is_superuser" bool NOT NULL, 
    "email" varchar(254) NOT NULL UNIQUE, 
    "is_company" bool NOT NULL, 
    "is_staff" bool NOT NULL, 
    "is_active" bool NOT NULL, 
    "date_joined" datetime NOT NULL)
'''