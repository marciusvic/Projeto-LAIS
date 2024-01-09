from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from agendamento_covid.grupos import obter_grupos
from agendamento_covid.funcoes import validar_idade, validar_cpf

# Create your views herede
def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/homeLogado.html')
    else:
        return render(request, 'usuarios/home.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')
    else:
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        user = authenticate(request, cpf=cpf, senha=senha)
    
    if user:
        auth_login(request, user)
        return redirect('home')
    else:
        return render(request, 'usuarios/login.html', {'error_message': 'Usuário ou senha inválidos!'})


def cadastrar(request):
    if request.method == 'GET':
        lista_grupos = obter_grupos()
        context = {
            'grupos': lista_grupos
        }
        print(lista_grupos)
        return render(request, 'usuarios/cadastrar.html', context)
    else:
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        date_nascimento = request.POST.get('date_nascimento')
        grupo = request.POST.get('grupo')
        covid_30_dias = request.POST.get('covid_30_dias')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        if grupo == 'População Privada de Liberdade' or grupo == 'Pessoas com Deficiência Institucionalizadas' or grupo == 'ACAMADAS de 80 anos ou mais' or covid_30_dias or validar_idade(date_nascimento) < 18:
            apto = False
        else:
            apto = True

        #erros
        cpf = request.POST.get('cpf')
        cpf_existe = User.objects.filter(cpf=cpf).exists()
        if cpf_existe:
            return HttpResponse('CPF já cadastrado!')
        if cpf == '' or cpf == None or len(cpf) != 14:
            return HttpResponse('CPF inválido, você deve coloca-lo no formato xxx.xxx.xxx-xx!')
        if not validar_cpf(cpf):
            return HttpResponse('CPF inválido, o CPF deve ser composto apenas de números, no formato xxx.xxx.xxx-xx!')
        if validar_idade(date_nascimento) > 110 or validar_idade(date_nascimento) < 0:
            return HttpResponse('Data de nascimento inválida!')
        if senha != confirma_senha:
            return HttpResponse('Senhas não conferem!')
        
        user = User.objects.create_user(nome=nome, cpf=cpf, date_nascimento=date_nascimento, grupo=grupo, covid_30_dias=covid_30_dias, email=email, senha=senha, apto=apto)
        user.save()
        if user.apto:
            return HttpResponse('Usuário cadastrado com sucesso!')
        else:
            return HttpResponse('Usuário cadastrado com sucesso, porém não está apto para receber a vacina!')

def agendamento(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/agendamento.html')
    else:
        return redirect('')

