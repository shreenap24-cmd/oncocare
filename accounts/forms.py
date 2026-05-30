from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PatientProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['phone', 'date_of_birth', 'blood_group', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }