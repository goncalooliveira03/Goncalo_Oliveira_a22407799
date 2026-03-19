from django.db import models

class Receita(models.Model):
    nome = models.CharField(max_length=100)
