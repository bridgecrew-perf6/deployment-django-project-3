from django import forms
from django.db.models import fields
from learning_user_app.models import UserProfileInfo
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    email = forms.EmailField(widget=forms.EmailInput())
    verification_email = forms.EmailField(widget=forms.EmailInput())

    class Meta():
        model = User
        fields = ['username', 'email', 'verification_email', 'password', 'password_confirm']

    def clean(self):
        
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError("password and confirm_password does not match")
        return self.cleaned_data

    def clean_verification_email(self):
        email = self.cleaned_data['email']
        v_email = self.cleaned_data['verification_email']

        if email != v_email:
            raise ValidationError("verification Email is wrong !!!")


class UserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)
    class Meta():
        model = UserProfileInfo
        fields = ['profile_pic', 'profile_site']