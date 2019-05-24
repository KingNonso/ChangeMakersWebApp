from django import forms

from .models import Enquiry

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['first_name', 'last_name', 'phone_number','email', 'subject','message']

    def clean_subject(self):
        name = self.cleaned_data.get('subject')
        if name == 'Hello':
            raise forms.ValidationError('Not a valid name')
        return name
