from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Quote

    
class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        exclude = ['created_at', 'updated_at', 'owner',]
        labels = { 'text': _('Quote Text'), 'public_accessible': _('Public'), }
    
    def clean_text(self):
        data = self.cleaned_data['text']
        
        #check if empty
        if not text:
            raise ValidationError(_('Text Must Not Be Empty'))

        #check if whitespace
        if not text.strip():
            raise ValidationError(_('Text Must Not Be Only Whitespace'))

        # Remember to always return the cleaned data.
        return data