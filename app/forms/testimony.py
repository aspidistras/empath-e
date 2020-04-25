from django import forms
from django.forms import ModelForm, Textarea
from app.models.testimony import Testimony


class TestimonyForm(ModelForm):
    """Defines the testimony creating form's fields"""

    class Meta:
        """Customize Django's original ModelForm class"""

        model = Testimony

        # defines which fields are to be displayed
        fields = ['content']

        # defines the labels displayed
        labels = {
            'content': 'Saissisez ici votre témoignage ',
        }

        widgets = {
            'content': Textarea(attrs={'rows':10, 'cols':20}),
        }


