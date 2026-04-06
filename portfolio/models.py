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


class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20, blank=True)
    ano = models.IntegerField()  # 1º, 2º ou 3º ano
    semestre = models.CharField(max_length=50, null=True, blank=True)
    ects = models.IntegerField(default=6)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='ucs/', blank=True, null=True)
    docente = models.CharField(max_length=200, blank=True)
    link_docente = models.URLField(blank=True)
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.SET_NULL, null=True, blank=True, related_name='ucs')

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
    categoria = models.CharField(max_length=100, blank=True)  # ex: linguagem, framework, ferramenta

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    ano = models.IntegerField()
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    repositorio_github = models.URLField(blank=True)
    conceitos_aplicados = models.TextField(blank=True)
    unidade_curricular = models.ForeignKey(UnidadeCurricular, on_delete=models.SET_NULL, null=True, blank=True, related_name='projetos')
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='projetos')

    def __str__(self):
        return self.nome


class TFC(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200)
    ano = models.IntegerField()
    resumo = models.TextField(blank=True)
    orientador = models.CharField(max_length=200, blank=True)
    link = models.URLField(blank=True)
    destaque = models.BooleanField(default=False)  # para marcar os mais interessantes

    def __str__(self):
        return f"{self.titulo} ({self.ano})"


class Competencia(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True)
    projetos = models.ManyToManyField(Projeto, blank=True)

    def __str__(self):
        return self.nome


class Formacao(models.Model):
    nome = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    ano = models.IntegerField()
    descricao = models.TextField(blank=True)
    certificado = models.FileField(upload_to='formacoes/', blank=True, null=True)
    link = models.URLField(blank=True)

    class Meta:
        ordering = ['-ano']  # mais recente primeiro

    def __str__(self):
        return f"{self.nome} ({self.ano})"


class MakingOf(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)
    fotografia = models.ImageField(upload_to='makingof/', blank=True, null=True)
    erros_encontrados = models.TextField(blank=True)
    decisoes_tomadas = models.TextField(blank=True)
    uso_ia = models.TextField(blank=True)  # descrever uso de IA se aplicável
    entidade_relacionada = models.CharField(max_length=100, blank=True)  # ex: "Projeto", "UC", etc.

    def __str__(self):
        return f"{self.titulo} ({self.data})"