from django.test import TestCase
from carespace.models import CareSpace 
from django.db import IntegrityError

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
        with self.assertRaises(IntegrityError):
            self.create_carespace(headline = None)
            self.create_carespace(paid = None)
            self.create_carespace(rich_text = None)

        # invalid Type
        """
        self.assertRaises(self.create_carespace(headline = int_default))
        self.assertRaises(self.create_carespace(headline = boolean_default))
        self.assertRaises(self.create_carespace(headline = flaot_default))
        
        self.assertRaises(self.create_carespace(body = int_default))
        self.assertRaises(self.create_carespace(body = boolean_default))
        self.assertRaises(self.create_carespace(body = flaot_default))

        self.assertRaises(self.create_carespace(author = int_default))
        self.assertRaises(self.create_carespace(author = boolean_default))
        self.assertRaises(self.create_carespace(author = flaot_default))

        self.assertRaises(self.create_carespace(publisher = int_default))
        self.assertRaises(self.create_carespace(publisher = boolean_default))
        self.assertRaises(self.create_carespace(publisher = flaot_default))

        self.assertRaises(self.create_carespace(paid = int_default))
        self.assertRaises(self.create_carespace(paid = string_default))
        self.assertRaises(self.create_carespace(paid = float_default))

        self.assertRaises(self.create_carespace(rich_text = int_default))
        self.assertRaises(self.create_carespace(rich_text = string_default))
        self.assertRaises(self.create_carespace(rich_text = float_default))

        self.assertRaises(self.create_carespace(img_description = int_default))
        self.assertRaises(self.create_carespace(img_description = boolean_default))
        self.assertRaises(self.create_carespace(img_description = flaot_default))

        self.assertRaises(self.create_carespace(introduction = int_default))
        self.assertRaises(self.create_carespace(introduction = boolean_default))
        self.assertRaises(self.create_carespace(introduction = flaot_default))
        """

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
        cs = CareSpace.objects.create(
            headline = headline,
            body = body,
            author = author,
            publisher = publisher,
            paid = paid,
            rich_text = rich_text,
            img_description = img_description,
            introduction = introduction,
        )

        cs.save()

        return cs
