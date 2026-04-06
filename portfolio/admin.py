from django.contrib import admin
from .models import (
    Licenciatura, UnidadeCurricular, Tecnologia,
    Projeto, TFC, Competencia, Formacao, MakingOf
)


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sigla', 'instituicao', 'ano_inicio']
    search_fields = ['nome', 'sigla', 'instituicao']


@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ano', 'semestre', 'ects', 'docente']
    list_filter = ['ano', 'semestre']
    search_fields = ['nome', 'docente']


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nivel', 'categoria']
    list_filter = ['nivel', 'categoria']
    search_fields = ['nome']


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ano', 'unidade_curricular']
    list_filter = ['ano', 'unidade_curricular']
    search_fields = ['nome', 'descricao']
    filter_horizontal = ['tecnologias']


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'ano', 'destaque']
    list_filter = ['ano', 'destaque']
    search_fields = ['titulo', 'autor', 'orientador']


@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']
    filter_horizontal = ['tecnologias', 'projetos']


@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'instituicao', 'ano']
    list_filter = ['ano']
    search_fields = ['nome', 'instituicao']


@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data', 'entidade_relacionada']
    list_filter = ['data', 'entidade_relacionada']
    search_fields = ['titulo', 'descricao']