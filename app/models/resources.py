"""Resources page related models"""


from django.db import models


class Disorder(models.Model):
    """Model to store data on different mental disorders"""

    name = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)


class Link(models.Model):
    """Model to add links or structure names specialized in a perticular disorder"""

    content = models.CharField(max_length=300)
    disorder = models.ForeignKey(Disorder, on_delete=models.CASCADE)
