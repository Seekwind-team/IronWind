from django.test import TestCase, Client

from joboffer.models import JobOffer, Authentication

class JobOfferTestCase(TestCase):
    def setUp(self):
    
        # maximal filled JobOffer
        max_joboffer = JobOffer.objects.create(
            #owner = TBD
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
            # created_at and last_modified are set to default (now),
        )

        # minimal filled JobOffer
        min_joboffer = JobOffer.objects.create(
            owner = owner,
            job_title = 'min Jobangebot',
            # created_at and last_modified are set to default (now),
        )

        max_joboffer.save()
        min_joboffer.save()

    def test_job_offer_to_string(self):
        max_joboffer = JobOffer.objects.get(job_title='max Jobangebot')
        min_joboffer = JobOffer.objects.get(job_title='min Jobangebot')

        # .._joboffer.pk might cause errors, if so try .._joboffer.id
        max_str = 'Joboffer ({}) "{}"'.format(max_joboffer.pk, max_joboffer.job_title)
        min_str = 'Joboffer ({}) "{}"'.format(min_joboffer.pk, min_joboffer.job_title)

        self.assertEqual(max_str, max_joboffer.__str__())
        self.assertEqual(min_str, min_joboffer.__str__())