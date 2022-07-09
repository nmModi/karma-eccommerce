from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), )
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Repeat your password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email..'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
        }
        labels = {
            'email': '',
            'username': '',
            'first_name': '',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']