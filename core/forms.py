from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Quote

    
class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        exclude = ['created_at', 'updated_at', 'owner', 'last_accessed',]
        labels = { 'text': _(''), 'public_accessible': _('Public'), }
        widgets = {
            'text': forms.Textarea({
                'class': 'form-control', 
                # 'style': 'resize:none',
                }),
        }
    
    def clean_text(self):
        data = self.cleaned_data['text']
        
        #check if empty
        if not data:
            raise ValidationError(_('Text Must Not Be Empty'))

        #check if whitespace
        if not data.strip():
            raise ValidationError(_('Text Must Not Be Only Whitespace'))

        # Remember to always return the cleaned data.
        return data

# class QuoteEntryForm(forms.Form):
#     quote_text = forms.CharField(widget= forms.Textarea, label="quote text", required=True, help_text="enter quote text")
#     public_accessible = forms.BooleanField(required=False, label="public")

#     def clean_quote_text(self):
#         data = self.cleaned_data['quote_text']

#         #check quote text isn't empty
#         if not data or data.isspace():
#             raise ValidationError(_('Text cannot be empty'))

#         #return cleaned data
#         return data
