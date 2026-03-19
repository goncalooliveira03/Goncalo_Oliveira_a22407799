from django.db import models

class Aplicacao_do_quizz(models.Model):
    nome = models.CharField(max_length=100)