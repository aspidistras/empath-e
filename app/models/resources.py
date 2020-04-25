"""Resources page related models"""


from django.db import models


class Disorder(models.Model):
    """Model to store data on different mental disorders"""

    name = models.CharField(max_length=100, unique=True)
    details = models.CharField(max_length=1000)
    url_pattern = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Link(models.Model):
    """Model to add links or structure names specialized in a perticular disorder"""

    content = models.CharField(max_length=300, unique=True)
    disorder = models.ForeignKey(Disorder, on_delete=models.CASCADE)
