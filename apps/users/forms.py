from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from apps.users.models import User


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, required=True, help_text='Enter your phone number')
    password = forms.CharField(max_length=15, required=True, help_text='Enter you password')

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')

        if phone_number and password:
            cleaned_data = super().clean()
            if phone_number and password:
                user = User.objects.filter(phone_no=phone_number).first()
                if user and not user.is_active:
                    raise forms.ValidationError(
                        "User is Inactive. Please contact the Administrator"
                    )
                if user and user.is_superuser:
                    user = authenticate(username=phone_number, password=password)
                    if not user:
                        raise forms.ValidationError(
                            "Username or password is incorrect"
                        )
                cleaned_data.update({'user': user})

        return super().clean()


class SignupForm(forms.ModelForm):
    password = forms.CharField(max_length=15, required=True, help_text='Enter you password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_no', 'password', 'dob', 'gender']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'dob', 'gender']