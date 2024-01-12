from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    nome = models.CharField(max_length=100, blank=False, null=False)
    cpf = models.CharField(max_length=11, unique=True, blank=False, null=False)
    date_nascimento = models.DateField(blank=False, null=False)
    grupo = models.CharField(max_length=100, blank=False, null=False)
    covid_30_dias = models.BooleanField(default=False)
    apto = models.BooleanField(default=False, blank=False, null=False)

class Agendamento(models.Model):
    id_usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data_agendamento = models.DateField()
    hora_agendamento = models.TimeField()
    cod_unidade = models.CharField(max_length=255)