from django.contrib.auth.forms import UserCreationForm
from .models import User,Address
from django import forms

class customForm(UserCreationForm):
    firstname=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter first name'}))
    lastname=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter last name'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter E-mail id'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))
    
    class Meta:
        model=User
        fields=['firstname','lastname','email','password1','password2']


class AddressForm(forms.ModelForm):
    model=Address
    fields='__all__'