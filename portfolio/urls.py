from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('licenciaturas/', views.licenciaturas_view, name='licenciaturas'),
    path('docentes/', views.docentes_view, name='docentes'),
    path('ucs/', views.ucs_view, name='ucs'),
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('projetos/', views.projetos_view, name='projetos'),
    path('competencias/', views.competencias_view, name='competencias'),
    path('formacoes/', views.formacoes_view, name='formacoes'),
    path('tfcs/', views.tfcs_view, name='tfcs'),
    path('makingof/', views.makingof_view, name='makingof'),
    path('', views.projetos_view),
    path('projetos/novo/', views.projeto_criar, name='projeto_criar'),
    path('projetos/<int:pk>/editar/', views.projeto_editar, name='projeto_editar'),
    path('projetos/<int:pk>/apagar/', views.projeto_apagar, name='projeto_apagar'),
    path('tecnologias/nova/', views.tecnologia_criar, name='tecnologia_criar'),
    path('tecnologias/<int:pk>/editar/', views.tecnologia_editar, name='tecnologia_editar'),
    path('tecnologias/<int:pk>/apagar/', views.tecnologia_apagar, name='tecnologia_apagar'),
    path('competencias/nova/', views.competencia_criar, name='competencia_criar'),
    path('competencias/<int:pk>/editar/', views.competencia_editar, name='competencia_editar'),
    path('competencias/<int:pk>/apagar/', views.competencia_apagar, name='competencia_apagar'),
    path('formacoes/nova/', views.formacao_criar, name='formacao_criar'),
    path('formacoes/<int:pk>/editar/', views.formacao_editar, name='formacao_editar'),
    path('formacoes/<int:pk>/apagar/', views.formacao_apagar, name='formacao_apagar'),
    path('sobre/', views.sobre_view, name='sobre'),
]