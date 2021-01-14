from django.test import TestCase, Client

from joboffer.models import JobOffer, Authentication
from user.tests import CreateUser
from django.db import IntegrityError
from django.core.exceptions import ValidationError
class JobOfferTests(TestCase):
    def setUp(self):
        user_created = False
        email_nr = 0
        self.pw = "123"

        while not user_created: 
            if CreateUser.create_user(self, email = "user{}@demo.de".format(email_nr), pw = self.pw):
                user_created = True
            else:
                email_nr += 1
        
        self.email = "user{}@demo.de".format(email_nr)
        self.user = Authentication.objects.filter(email=self.email).get()


    # test every accepted job_type
    def test_job_type(self):
        job_types = JobOffer.JOBTYPE_CHOICES
        
        for choice in job_types:
            job_offer = self.create_joboffer(owner=self.user, job_type=choice)
            self.assertEqual(job_offer.job_type, choice)
        
        
    def test_none_parameters(self):
        with self.assertRaises(IntegrityError):
            self.create_joboffer(owner=self.user, filled=None)
            self.create_joboffer(owner=self.user, is_deleted=None)
            self.create_joboffer(owner=self.user, job_type=None)
            self.create_joboffer(owner=self.user, job_title=None)
            self.create_joboffer(owner=self.user, location=None)
            self.create_joboffer(owner=self.user, description=None)
            self.create_joboffer(owner=self.user, highlights=None)
            self.create_joboffer(owner=self.user, must_have=None)
            self.create_joboffer(owner=self.user, nice_have=None)
            self.create_joboffer(owner=self.user, public_email=None)
            self.create_joboffer(owner=self.user, pay_per_year=None)
            self.create_joboffer(owner=self.user, city=None)
            self.create_joboffer(owner=self.user, start_date=None)
            self.create_joboffer(owner=self.user, trade=None)

    def test_invalid_parameters(self):
        int_default = 42
        # if you want to change demo_string do not use a String that matches any entry in job_type ENUM or any email (just avoid @ and .).
        string_default = "demostring"
        boolean_default = False
        float_default = 4.2
            
        with self.assertRaises(ValidationError):
            self.create_joboffer(owner=self.user, filled=int_default)
            self.create_joboffer(owner=self.user, filled=string_default)
            self.create_joboffer(owner=self.user, filled=float_default)

            self.create_joboffer(owner=self.user, is_deleted=int_default)
            self.create_joboffer(owner=self.user, is_deleted=string_default)
            self.create_joboffer(owner=self.user, is_deleted=float_default)

            self.create_joboffer(owner=self.user, job_type=int_default)
            self.create_joboffer(owner=self.user, job_type=string_default)
            self.create_joboffer(owner=self.user, job_type=boolean_default)
            self.create_joboffer(owner=self.user, job_type=float_default)

            self.create_joboffer(owner=self.user, job_title=int_default)
            self.create_joboffer(owner=self.user, job_title=string_default)
            self.create_joboffer(owner=self.user, job_title=float_default)

            self.create_joboffer(owner=self.user, location=int_default)
            self.create_joboffer(owner=self.user, location=string_default)
            self.create_joboffer(owner=self.user, location=boolean_default)

            self.create_joboffer(owner=self.user, description=int_default)
            self.create_joboffer(owner=self.user, description=boolean_default)
            self.create_joboffer(owner=self.user, description=float_default)

            self.create_joboffer(owner=self.user, highlights=int_default)
            self.create_joboffer(owner=self.user, highlights=boolean_default)
            self.create_joboffer(owner=self.user, highlights=float_default)

            self.create_joboffer(owner=self.user, must_have=int_default)
            self.create_joboffer(owner=self.user, must_have=boolean_default)
            self.create_joboffer(owner=self.user, must_have=float_default)

            self.create_joboffer(owner=self.user, nice_have=int_default)
            self.create_joboffer(owner=self.user, nice_have=boolean_default)
            self.create_joboffer(owner=self.user, nice_have=float_default)
            
            self.create_joboffer(owner=self.user, public_email=int_default)
            self.create_joboffer(owner=self.user, public_email=string_default)
            self.create_joboffer(owner=self.user, public_email=boolean_default)
            self.create_joboffer(owner=self.user, public_email=float_default)
            
            self.create_joboffer(owner=self.user, pay_per_year=int_default)
            self.create_joboffer(owner=self.user, pay_per_year=string_default)
            self.create_joboffer(owner=self.user, pay_per_year=boolean_default)

            self.create_joboffer(owner=self.user, city=int_default)
            self.create_joboffer(owner=self.user, city=string_default)
            self.create_joboffer(owner=self.user, city=boolean_default)

            self.create_joboffer(owner=self.user, start_date=int_default)
            self.create_joboffer(owner=self.user, start_date=string_default)
            self.create_joboffer(owner=self.user, start_date=boolean_default)

            self.create_joboffer(owner=self.user, trade=int_default)
            self.create_joboffer(owner=self.user, trade=string_default)
            self.create_joboffer(owner=self.user, trade=boolean_default)


    def test_job_offer_to_string(self):
        # maximal filled JobOffer
        max_joboffer = self.create_joboffer( owner = self.user)
        
        # minimal filled JobOffer
        min_joboffer = JobOffer.objects.create(
            owner = self.user,
            job_title = 'min Jobangebot',
        )

        max_str = 'Joboffer ({}) "{}"'.format(max_joboffer.pk, max_joboffer.job_title)
        min_str = 'Joboffer ({}) "{}"'.format(min_joboffer.pk, min_joboffer.job_title)

        self.assertEqual(max_str, max_joboffer.__str__())
        self.assertEqual(min_str, min_joboffer.__str__())


    # creates JobOffer
    # self and owner parameter are neccesary. To create an owner use create_user from user/tests.py
    # created_at and last_modified are set to default (now)
    # public email default is owner email
    def create_joboffer(
        self,
        owner,
        public_email = None,
        filled = False,
        is_deleted = False,
        job_type = 'Vollzeit',
        job_title = 'max Jobangebot',
        location = 'Heidenheim',
        description = 'das ist 1 guter Job',
        highlights = 'ganz viele',
        must_have = 'alle bitte',
        nice_have = 'öalsidhf',
        pay_per_year = '777,1230,13',
        city = 'Engelsberg',
        start_date = '2020-11-23',
        trade = 'Arbeiter',
        ):
        if public_email is None:
            public_email = owner.email

        job_offer = JobOffer.objects.create(
            owner = owner,
            filled = filled,
            is_deleted = is_deleted,
            job_type = job_type,
            job_title = job_title,
            location = location,
            description = description,
            highlights = highlights,
            must_have = must_have,
            nice_have = nice_have,
            public_email = public_email,
            pay_per_year = pay_per_year,
            city = city,
            start_date = start_date,
            trade = trade
        )
        
        job_offer.save()

        return job_offer