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
]