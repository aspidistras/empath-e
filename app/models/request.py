"""Contact requests related models and filters"""

import django_filters

from django.db import models
from django.contrib.auth.models import User
from app.models.resources import Disorder


class Request(models.Model):
    """Model to store data on contact requests"""

    STATUS = [
        (0, 'Requête envoyée.'),
        (1, 'Requête acceptée, session d\'échange à venir.'), 
        (3, 'Rendez-vous terminé, requête archivée.'),
    ]

    disorder = models.ForeignKey(Disorder, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='want_to_understand_user')
    status = models.IntegerField(choices=STATUS, default=0)
    awareness_user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None,
                                       related_name='raise_awareness_user', null=True)


class RequestFilter(django_filters.FilterSet):
    """FilterSet to get requests from specified disorder"""

    disorder = django_filters.ModelChoiceFilter(queryset=Disorder.objects.all(), label="Concernant ce trouble ")

    class Meta:
        model = Request
        fields = ['disorder']
