from django import forms


class ContactForm(forms.Form):
    """Defines the contact form's fields"""

    email = forms.EmailField(required=True, label='Votre mail ')
    subject = forms.CharField(required=True, label='Au sujet de ')
    message = forms.CharField(widget=forms.Textarea, required=True, label='Écrivez ici votre message ')
