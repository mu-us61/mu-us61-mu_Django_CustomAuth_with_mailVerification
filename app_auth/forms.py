from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm  
from . import models

# TODO password1 ve password2 eşleşecekmi validate
# TODO username dublicated ve mail bakılacak

class CustomForm(forms.Form):
    username_validator = UnicodeUsernameValidator(
        message=_(
            "Enter a valid username. This value may contain only letters, "
            "numbers, and @/./+/-/_ characters."
        )
    )


    username = forms.CharField(
        label="username_label",
        max_length=128,
        required=True,
        validators=[username_validator],

        widget=forms.TextInput(
        attrs={
        'class':'form-input',
        'placeholder':'Username'
        }
        ),
    )
    password1 = forms.CharField(label="password1_label", max_length=128, required=True,
    widget=forms.PasswordInput(
        attrs={
            'class':'form-input',
            'placeholder':'password'
        }
    ))
    password2 = forms.CharField(label="password2_label", max_length=128, required=True,
    widget=forms.PasswordInput(
        attrs={
            'class':'form-input',
            'placeholder':'password'
        }
    ))
    email = forms.EmailField(label="email_label", required=True,
    widget=forms.EmailInput(
        attrs={'class':'form-input',
            'placeholder':'email'}
    ))

    def clean_username(self):
        data = self.cleaned_data['username'].lower()
        new = models.CustomUser.objects.filter(username = data)  
        if new.count():  
            raise forms.ValidationError("User Already Exist")  
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data  



    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password1")
        pass2 = cleaned_data.get("password2")

        if pass1 and pass2 and pass1!=pass2:
            raise forms.ValidationError("passwords did not match")

    def clean_email(self):
        data = self.cleaned_data['email'].lower()
        new = models.CustomUser.objects.filter(email = data)  
        if new.count():  
            raise forms.ValidationError("email already in use")
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data  

    # def save(self):
    #     pass
