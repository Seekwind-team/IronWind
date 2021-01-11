from django.test import TestCase
from django.contrib.auth.hashers import make_password

from user.models import *

class SimpleTest(TestCase):
    def setUp(self):
        self.email = "demo@user.de"
        self.pw = "123asdf"
        #self.create_user(self.email, self.pw)
        user = Authentication(is_superuser=False, password=self.pw, email=self.email)
        user.save()

    def test_credentials(self):
        user_object = Authentication.objects.get(email=self.email)
        self.assertEqual(user_object.email, self.email)
        self.assertEqual(user_object.password, make_password(self.pw))

    def create_user(self, email, pw):
        # user with email already exists exception
        
        Authentication.objects.raw('''
            INSERT into user_authentication (
                password, 
                email, 
                is_superuser, 
                is_company, 
                is_superuser,
                is_active, 
                is_staff, 
                last_login, 
                date_joined) 
            VALUES (
                '{password}',
                '{email}', 
                false, 
                true, 
                false, 
                true, 
                false, 
                {now}, 
                {now})
        '''.format(password = make_password(pw), email = email, now = now))
        
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