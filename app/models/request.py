"""Contact requests related models"""


from django.db import models
from django.contrib.auth.models import User
from app.models.resources import Disorder


class Request(models.Model):
    """Model to store data on contact requests"""

    STATUS = [
        (0, 'Requête envoyée.'),
        (1, 'Requête acceptée, un utilisateur va vous contacter !'),
        (2, 'Session d\'échange à venir.'), 
        (3, 'Rendez-vous terminé, requête archivée.'),
    ]

    disorder = models.ForeignKey(Disorder, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
