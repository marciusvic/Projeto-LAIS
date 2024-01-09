from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views herede
def home(request):
    return render(request, 'usuarios/home.html')

def login(request):
    return render(request, 'usuarios/login.html')

def cadastrar(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastrar.html')
    else:
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        date_nascimento = request.POST.get('date_nascimento')
        grupo = request.POST.get('grupo')
        covid_30_dias = request.POST.get('covid_30_dias')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        cpf_existe = User.objects.filter(cpf=cpf).exists()

        if cpf_existe:
            return HttpResponse('CPF já cadastrado!')
        if senha != confirma_senha:
            return HttpResponse('Senhas não conferem!')
        if cpf == '' or cpf == None or len(cpf) != 14:
            return HttpResponse('CPF inválido, você deve coloca-lo no formato xxx.xxx.xxx-xx!')
        
        return HttpResponse(date_nascimento)

def agendamento(request):
    return render(request, 'usuarios/agendamento.html')

def homeLogado(request):
    return render(request, 'usuarios/homeLogado.html')