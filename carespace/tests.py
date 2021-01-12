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
            # TODO this Attributes require uploads
            #header_image =
            #favicon_publisher =
        )

        # minimal filled care space
        CareSpace.objects.create(
            headline = "demo Headline min",
        )
        
        self.max_carespace = CareSpace.objects.get(headline = "demo Headline max")
        self.min_carespace = CareSpace.objects.get(headline = "demo Headline min")
        

    def test_carespace_to_string(self):
        max_str = "ID {}: {}".format(self.max_carespace.pk, self.max_carespace.headline)
        min_str = "ID {}: {}".format(self.min_carespace.pk, self.min_carespace.headline)
        
        self.assertEqual(max_str, self.max_carespace.__str__())
        self.assertEqual(min_str, self.min_carespace.__str__())

    def test_carespace_wrong_attr(self):
        pass