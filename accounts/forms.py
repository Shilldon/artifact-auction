from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Profile

class UserLoginForm(forms.Form):
    """Login form for existing users"""
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    """Registration form for new users"""
    
    password1 = forms.CharField(
        label="Enter password",
        widget=forms.PasswordInput)
        
    password2 = forms.CharField(
        label="Re-enter password",
        widget=forms.PasswordInput)     
    
    email = forms.EmailField(required=True)
    
    first_name = forms.CharField(
        label="First Name",
        max_length=50)

    last_name = forms.CharField(
        label="Last Name",
        max_length=50)

    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password1', 
            'password2', 
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError(u'Please enter an email address')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email):
            raise forms.ValidationError(u'That email address is already registered')
    
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(u'Please enter a username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username):
            raise forms.ValidationError(u'That username is already taken')
    
        return username
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        # Check that passwords have been completed in both fields and match.
        # Form validation should prevent the user from failing to complete
        # both password fields. This is a double check.
        if not password1:
            raise ValidationError(u'You need to enter a password')
        elif not password2:
            raise ValidationError(u'Please re-enter your password')
        elif password1 != password2:
            raise ValidationError(u'Passwords do not match')
    
        return password2

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'remain_anonymous', 'profile_picture')

    def name(self):
        self.fields['profile_picture'].label = "Choose file"

class UserEditProfileForm(UserChangeForm):
  
    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name', 
            'username', 
            'email',
            'password',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(u'Please enter an email address')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email):
            raise forms.ValidationError(u'That email address is already registered')
    
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(u'Please enter a username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username):
            raise forms.ValidationError(u'That username is already taken')
    
        return username