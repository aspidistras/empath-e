from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserForm(ModelForm):
    """Defines the account creating form's fields"""

    password = forms.CharField(widget=forms.PasswordInput(), label='Mot de passe ')

    class Meta:
        """Customize Django's original UserForm class"""

        model = User
        # defines which fields are to be displayed
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        help_texts = {
            'username': '',
        }
        # defines the labels displayed
        labels = {
            'username': 'Pseudo ', 'first_name': 'Prénom ', 'last_name': 'Nom ',
            'email': 'Email ',
        }
