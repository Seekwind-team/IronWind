from django.test import TestCase
from carespace.models import CareSpace 

class CareSpaceTestCase(TestCase):
    def setUp(self):
        # maximal filled care space
        CareSpace.objects.create(
            headline = "demo Headline max",
            body = "LoremipsumLoremipsumLoremipsumLoremipsumLoremipsumLoremipsum",
            author = "demo Author",
            publisher = "demo Publisher",
            paid = True,
            rich_text = True,
            img_description = "no image provided yet",
            introduction = "This is a Demo CareSpace",
            # tbd. this Attributes require uploads
            #header_image =
            #favicon_publisher =
        )

        # minimal filled care space
        CareSpace.objects.create(
            headline = "demo Headline min",
        )

    def test_carespace_to_string(self):
        max_carespace = CareSpace.objects.get(headline = "demo Headline max")
        min_carespace = CareSpace.objects.get(headline = "demo Headline min")
        
        max_str = "ID {}: {}".format(max_carespace.pk, max_carespace.headline)
        min_str = "ID {}: {}".format(min_carespace.pk, min_carespace.headline)
        
        self.assertEqual(max_str, max_carespace.__str__())
        self.assertEqual(min_str, min_carespace.__str__())
