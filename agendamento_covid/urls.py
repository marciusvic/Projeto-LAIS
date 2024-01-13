from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('agendamento/', views.agendamento, name='agendamento'),
    path('agendamento/<int:cod_unidade>/<str:data>/', views.selecionar_horario, name='selecionar_horario'),
    path('listar_agendamentos/', views.listar_agendamentos, name='listar_agendamentos'),
    path('logout/', views.logout_view, name='logout'),
]
