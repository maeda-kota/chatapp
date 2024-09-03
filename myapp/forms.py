from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class signupform(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Emailadress'
    )

    # img = forms.ImageField(
    #     required=True    
    # )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'img')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

# class LoginForm(AuthenticationForm):

#     def__init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
