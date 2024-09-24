from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class signupform(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Emailadress'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'img')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser

class usernameChangeform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)
       
class emailChangeform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class iconChangeform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('img',)

class passwordChangeform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('password',)


