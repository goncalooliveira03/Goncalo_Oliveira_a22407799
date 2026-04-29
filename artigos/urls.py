from django.urls import path
from . import views

app_name = 'artigos'

urlpatterns = [
    path('', views.lista_artigos, name='lista'),
    path('novo/', views.criar_artigo, name='criar'),
    path('<int:pk>/', views.detalhe_artigo, name='detalhe'),
    path('<int:pk>/editar/', views.editar_artigo, name='editar'),
    path('<int:pk>/apagar/', views.apagar_artigo, name='apagar'),
    path('<int:pk>/like/', views.like_artigo, name='like'),
]