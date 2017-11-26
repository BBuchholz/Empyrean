from django.test import TestCase
from core.models import Quote

class QuoteTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        #setup non-modified objects used by all test methods
        Quote.objects.create(text='A test quote', public_accessible=True)

    def test_text_label(self):
        quote = Quote.objects.get(id=1)
        field_label = quote._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_public_accessible_label(self):
        quote = Quote.objects.get(id=1)
        field_label = quote._meta.get_field('public_accessible').verbose_name
        self.assertEquals(field_label, 'public accessible')

    def test_get_absolute_url(self):
        quote = Quote.objects.get(id=1)
        #this will also fail if the urlconf is not defined
        self.assertEquals(quote.get_absolute_url(), '/quotes/1')

