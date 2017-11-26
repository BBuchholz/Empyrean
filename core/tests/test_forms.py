from django.test import TestCase

from core.forms import QuoteForm

class QuoteFormTestCase(TestCase):

    def test_text_field_label(self):
        form = QuoteForm()
        self.assertEquals(form.fields['text'].label, 'Quote Text')

    def test_public_accessible_field_label(self):
        form = QuoteForm()
        self.assertEquals(form.fields['public_accessible'].label, 'Public')

