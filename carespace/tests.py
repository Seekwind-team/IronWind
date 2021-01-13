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
        )

        # minimal filled care space
        CareSpace.objects.create(
            headline = "demo Headline min",
        )
        
        self.max_carespace = CareSpace.objects.get(headline = "demo Headline max")
        self.min_carespace = CareSpace.objects.get(headline = "demo Headline min")
        

    def test_carespace_invalid_creation(self):
        int_default = 42
        string_default = "text"
        boolean_default = False
        flaot_default = 4.2

        # None 
        self.assertError(create_carespace(self, headline = None))
        self.assertError(create_carespace(self, paid = None))
        self.assertError(create_carespace(self, rich_text = None))

        # invalid Type
        self.assertError(create_carespace(self, headline = int_default))
        self.assertError(create_carespace(self, headline = boolean_default))
        self.assertError(create_carespace(self, headline = flaot_default))
        
        self.assertError(create_carespace(self, body = int_default))
        self.assertError(create_carespace(self, body = boolean_default))
        self.assertError(create_carespace(self, body = flaot_default))

        self.assertError(create_carespace(self, author = int_default))
        self.assertError(create_carespace(self, author = boolean_default))
        self.assertError(create_carespace(self, author = flaot_default))

        self.assertError(create_carespace(self, publisher = int_default))
        self.assertError(create_carespace(self, publisher = boolean_default))
        self.assertError(create_carespace(self, publisher = flaot_default))

        self.assertError(create_carespace(self, paid = int_default))
        self.assertError(create_carespace(self, paid = string_default))
        self.assertError(create_carespace(self, paid = float_default))

        self.assertError(create_carespace(self, rich_text = int_default))
        self.assertError(create_carespace(self, rich_text = string_default))
        self.assertError(create_carespace(self, rich_text = float_default))

        self.assertError(create_carespace(self, img_description = int_default))
        self.assertError(create_carespace(self, img_description = boolean_default))
        self.assertError(create_carespace(self, img_description = flaot_default))

        self.assertError(create_carespace(self, introduction = int_default))
        self.assertError(create_carespace(self, introduction = boolean_default))
        self.assertError(create_carespace(self, introduction = flaot_default))
        

    def test_carespace_wrong_attr(self):
        pass
        max_str = "ID {}: {}".format(max_carespace.pk, max_carespace.headline)
        min_str = "ID {}: {}".format(min_carespace.pk, min_carespace.headline)
        
        self.assertEqual(max_str, max_carespace.__str__())
        self.assertEqual(min_str, min_carespace.__str__())
        

    def test_carespace_to_string(self):
        max_str = "ID {}: {}".format(self.max_carespace.pk, self.max_carespace.headline)
        min_str = "ID {}: {}".format(self.min_carespace.pk, self.min_carespace.headline)
        
        self.assertEqual(max_str, self.max_carespace.__str__())
        self.assertEqual(min_str, self.min_carespace.__str__())


    def create_carespace(
        self,
        headline = "demo Headline max",
        body = "LoremipsumLoremipsumLoremipsumLoremipsumLoremipsumLoremipsum",
        author = "demo Author",
        publisher = "demo Publisher",
        paid = True,
        rich_text = True,
        img_description = "no image provided yet",
        introduction = "This is a Demo CareSpace"
        ):
        return = CareSpace.objects.create(
            headline = headline,
            body = body,
            author = author,
            publisher = publisher,
            paid = paid,
            rich_text = rich_text,
            img_description = img_description,
            introduction = introduction,
        )
