from django.test import TestCase, Client

from joboffer.models import JobOffer, Authentication
from user.tests import UserTests

class JobOfferTestCase(TestCase):
    def setUp(self):
        user_created = False
        email_nr = 0
        self.pw = "123"

        while not user_created: 
            if UserTests.create_user(email = "user{}@demo.de".format(email_nr), pw = self.pw):
                user_created = True
            else:
                email_nr += 1
        
        self.email = "user{}@demo.de".format(email_nr)
        self.user = Authentication.objects.filter(email=self.email).get()

        max_joboffer.save()
        min_joboffer.save()

    # test every accepted job_type
    def test_job_type():
        job_types = JobOffer.JOBTYPE_CHOICES
    

    def test_invalid_parameters(self):
        int_default = 42
        # if you want to change demo_string do not use a String that matches any entry in job_type ENUM or any email (just avoid @ and .).
        string_default = "demostring"
        boolean_default = False
        float_default = 4.2
        
        # TODO commenting
        self.assertRaise(create_joboffer(owner=self.user, filled=int_default)) 
        self.assertRaise(create_joboffer(owner=self.user, filled=string_default)) 
        self.assertRaise(create_joboffer(owner=self.user, filled=float_default)) 

        self.assertRaise(create_joboffer(owner=self.user, is_deleted=int_default)) 
        self.assertRaise(create_joboffer(owner=self.user, is_deleted=string_default)) 
        self.assertRaise(create_joboffer(owner=self.user, is_deleted=float_default)) 

        self.assertRaise(create_joboffer(owner=self.user, job_type=int_default)) 
        self.assertRaise(create_joboffer(owner=self.user, job_type=)) 
        self.assertRaise(create_joboffer(owner=self.user, job_type=)) 
        self.assertRaise(create_joboffer(owner=self.user, job_type=)) 

        self.assertRaise(create_joboffer(owner=self.user, job_title=)) 
        self.assertRaise(create_joboffer(owner=self.user, job_title=)) 
        self.assertRaise(create_joboffer(owner=self.user, job_title=)) 

        self.assertRaise(create_joboffer(owner=self.user, location=)) 
        self.assertRaise(create_joboffer(owner=self.user, location=)) 
        self.assertRaise(create_joboffer(owner=self.user, location=)) 

        self.assertRaise(create_joboffer(owner=self.user, description=)) 
        self.assertRaise(create_joboffer(owner=self.user, description=)) 
        self.assertRaise(create_joboffer(owner=self.user, description=)) 

        self.assertRaise(create_joboffer(owner=self.user, highlights=)) 
        self.assertRaise(create_joboffer(owner=self.user, highlights=)) 
        self.assertRaise(create_joboffer(owner=self.user, highlights=)) 

        self.assertRaise(create_joboffer(owner=self.user, must_have=)) 
        self.assertRaise(create_joboffer(owner=self.user, must_have=)) 
        self.assertRaise(create_joboffer(owner=self.user, must_have=)) 

        self.assertRaise(create_joboffer(owner=self.user, nice_have=)) 
        self.assertRaise(create_joboffer(owner=self.user, nice_have=)) 
        self.assertRaise(create_joboffer(owner=self.user, nice_have=)) 

        self.assertRaise(create_joboffer(owner=self.user, public_email=)) 
        self.assertRaise(create_joboffer(owner=self.user, public_email=)) 
        self.assertRaise(create_joboffer(owner=self.user, public_email=)) 
        self.assertRaise(create_joboffer(owner=self.user, public_email=)) 

        self.assertRaise(create_joboffer(owner=self.user, pay_per_year=)) 
        self.assertRaise(create_joboffer(owner=self.user, pay_per_year=)) 
        self.assertRaise(create_joboffer(owner=self.user, pay_per_year=)) 

        self.assertRaise(create_joboffer(owner=self.user, city=)) 
        self.assertRaise(create_joboffer(owner=self.user, city=)) 
        self.assertRaise(create_joboffer(owner=self.user, city=)) 

        self.assertRaise(create_joboffer(owner=self.user, start_date=)) 
        self.assertRaise(create_joboffer(owner=self.user, start_date=)) 
        self.assertRaise(create_joboffer(owner=self.user, start_date=)) 

        self.assertRaise(create_joboffer(owner=self.user, trade=)) 
        self.assertRaise(create_joboffer(owner=self.user, trade=)) 
        self.assertRaise(create_joboffer(owner=self.user, trade=)) 

    def test_job_offer_to_string(self):
        # maximal filled JobOffer
        max_joboffer = create_joboffer(self, owner = self.user)
        
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
        #hashtags = TBD,
        filled = False,
        is_deleted = False,
        job_type = 'Vollzeit',
        job_title = 'max Jobangebot',
        location = 'Heidenheim',
        description = 'das ist 1 guter Job',
        highlights = 'ganz viele',
        must_have = 'alle bitte',
        nice_have = 'öalsidhf',
        public_email = owner.email,
        pay_per_year = '777,1230,13',
        city = 'Engelsberg',
        start_date = '2020-11-23',
        trade = 'Arbeiter',
        ):
        return JobOffer.objects.create(
            owner = owner,
            #hashtags = TBD,
            filled = filled,
            is_deleted = is_deleted,
            job_type = job_type,
            job_title = job_title,
            location = locations,
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