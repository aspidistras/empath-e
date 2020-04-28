"""Testimonies page related models"""


from django.db import models
from django.contrib.auth.models import User

from app.models.resources import Disorder


class Testimony(models.Model):
    """Model to store data on testimonies"""

    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disorder = models.ForeignKey(Disorder, on_delete=models.CASCADE, null=True)
