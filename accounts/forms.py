from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class PhoneForm(forms.Form):
    phone_number = forms.CharField(required=True, label="Phone number:")


class RegistrationForm(UserCreationForm):
    '''Var #2:
    - User doesnotexist
    - Model Users is empty '''
    first_name = forms.CharField(required=True, label="First name:", max_length=100)
    last_name = forms.CharField(required=True, label="Last name:", max_length=100)
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    otp_code = forms.CharField(required=True, max_length=4)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1', 'password2', 'otp_code')


class RegistrationForm2(forms.Form):
    '''Var #1:
        - User doesnotexist
        - Model User has a records'''
    first_name = forms.CharField(required=True, label="First name:", max_length=100)
    last_name = forms.CharField(required=True, label="Last name:", max_length=100)
    otp_code = forms.CharField(required=True, label="OTP code", max_length=4)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'otp_code')


class LoginForm(forms.Form):
    '''Var #3:
        - User is exist
        - User is an employee '''
    otp_code = forms.CharField(required=True, max_length=4)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('otp_code', 'password')


class LoginForm2(forms.Form):
    '''Var #4:
        - User is exist
        - User is not an employee '''
    prefix = 'LoginForm2'
    otp_code = forms.CharField(required=True, max_length=4)
