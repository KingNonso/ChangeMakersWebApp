# accounts.forms.py
from django import forms
from django.contrib.auth import get_user_model

from accounts.models import MEMBERSHIP_TYPE, Member


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2', 'is_active')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = get_user_model().objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Email already exists, cannot use this email")
        return email


class MembershipForm(forms.ModelForm):
    membership_type= forms.CharField(label='Select Membership Type', widget=forms.Select(choices=MEMBERSHIP_TYPE))
    dob = forms.DateField(label='Date of Birth' ,input_formats=['%d/%m/%Y'])

    class Meta:
        model = Member
        fields = ('other_name', 'primary_phone', 'secondary_phone', 'membership_type', 
                    'nse_no', 'coren_no', 'dob', 'address', 'work', 'job', 'bio', 'photo', 'gender')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
