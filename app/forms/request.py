from django import forms
from django.forms import ModelForm
from app.models.requests import Request
from app.models.resources import Disorder


class RequestForm(ModelForm):
    """Defines the request creating form's fields"""

    disorders = forms.ModelChoiceField(queryset=Disorder.objects.all(), required=True, label='A propos du trouble suivant ', to_field_name="name")

    class Meta:
        """Customize Django's original ModelForm class"""

        model = Request

        # defines which fields are to be displayed
        fields = ['disorders', 'message']

        # defines the labels displayed
        labels = {
            'message': 'Expliquez votre requête en quelques mots ',
        }


