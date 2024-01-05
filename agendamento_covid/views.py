from django.shortcuts import render
from django.http import HttpResponse

# Create your views herede
def home(request):
    return render(request, 'usuarios/home.html')

def login(request):
    return render(request, 'usuarios/login.html')

def cadastrar(request):
    return render(request, 'usuarios/cadastrar.html')

def agendamento(request):
    return render(request, 'usuarios/agendamento.html')

def homeLogado(request):
    return render(request, 'usuarios/homeLogado.html')