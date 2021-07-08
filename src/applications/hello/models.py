from django.db import models


class HelloModel(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    background_color = models.TextField(null=True, blank=True)
    text_color = models.TextField(null=True, blank=True)

