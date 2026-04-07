from django.db import models


class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    instituicao = models.CharField(max_length=200)
    ano_inicio = models.IntegerField()
    descricao = models.TextField(blank=True)
    link = models.URLField(blank=True)
    logo = models.ImageField(upload_to='licenciatura/', blank=True, null=True)

    def __str__(self):
        return f"{self.sigla} - {self.instituicao}"


class Docente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    link_pagina_lusofona = models.URLField(blank=True)
    fotografia = models.ImageField(upload_to='docentes/', blank=True, null=True)
    departamento = models.CharField(max_length=200, blank=True)
    especialidade = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nome


class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20, blank=True)
    ano = models.IntegerField()
    semestre = models.IntegerField()
    ects = models.IntegerField(default=6)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='ucs/', blank=True, null=True)
    licenciatura = models.ForeignKey(
        Licenciatura, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ucs'
    )
    docentes = models.ManyToManyField(
        Docente, blank=True, related_name='ucs'
    )

    def __str__(self):
        return f"{self.nome} ({self.ano}º ano)"


class Tecnologia(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermédio'),
        ('avancado', 'Avançado'),
    ]
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    logo = models.ImageField(upload_to='tecnologias/', blank=True, null=True)
    link_oficial = models.URLField(blank=True)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='basico')
    categoria = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    ano = models.IntegerField()
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    repositorio_github = models.URLField(blank=True)
    link_deploy = models.URLField(blank=True)
    conceitos_aplicados = models.TextField(blank=True)
    competencias_adquiridas = models.TextField(blank=True)
    colaboradores = models.CharField(max_length=300, blank=True)
    unidade_curricular = models.ForeignKey(
        UnidadeCurricular, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='projetos'
    )
    tecnologias = models.ManyToManyField(
        Tecnologia, blank=True, related_name='projetos'
    )

    def __str__(self):
        return self.nome


class Competencia(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tecnologias = models.ManyToManyField(
        Tecnologia, blank=True, related_name='competencias'
    )
    projetos = models.ManyToManyField(
        Projeto, blank=True, related_name='competencias'
    )

    def __str__(self):
        return self.nome


class Formacao(models.Model):
    nome = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    ano = models.IntegerField()
    descricao = models.TextField(blank=True)
    certificado = models.FileField(upload_to='formacoes/', blank=True, null=True)
    link = models.URLField(blank=True)
    competencias = models.ManyToManyField(
        Competencia, blank=True, related_name='formacoes'
    )

    class Meta:
        ordering = ['-ano']

    def __str__(self):
        return f"{self.nome} ({self.ano})"


class TFC(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200)
    ano = models.IntegerField()
    resumo = models.TextField(blank=True)
    orientador = models.ForeignKey(
        Docente, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tfcs'
    )
    link = models.URLField(blank=True)
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} ({self.ano})"


class MakingOf(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)
    fotografia = models.ImageField(upload_to='makingof/', blank=True, null=True)
    erros_encontrados = models.TextField(blank=True)
    decisoes_tomadas = models.TextField(blank=True)
    uso_ia = models.TextField(blank=True)
    entidade_relacionada = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.data})"