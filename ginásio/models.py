from django.db import models

class Ginasio(models.Model):
    nome = models.CharField(max_length=100)
