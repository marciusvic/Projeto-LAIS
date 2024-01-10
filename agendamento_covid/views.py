from django.shortcuts import render, redirect
from django.http import HttpResponse
from agendamento_covid.models import CustomUser
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from agendamento_covid.grupos import obter_grupos
from agendamento_covid.funcoes import validar_idade, validar_cpf_digitos, validar_cpf_tamanho, verificar_apto, criar_username

def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/homeLogado.html', {'user_apto': request.user.apto})
    else:
        return render(request, 'usuarios/home.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def login(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')
    else:
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        username = CustomUser.objects.get(cpf=cpf).username

        user = authenticate(request, username=username, password=senha)
        
    if user:
        auth_login(request, user)
        return redirect('/')
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
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        if verificar_apto(grupo, covid_30_dias, validar_idade(date_nascimento)):
            apto = True

        cpf = request.POST.get('cpf')
        cpf_existe = CustomUser.objects.filter(cpf=cpf).exists()
        if cpf_existe:
            return HttpResponse('CPF já cadastrado!')
        if not validar_cpf_tamanho(cpf):
            return HttpResponse('CPF inválido, você deve coloca-lo no formato xxx.xxx.xxx-xx!')
        if not validar_cpf_digitos(cpf):
            return HttpResponse('CPF inválido, o CPF deve ser composto apenas de números, no formato xxx.xxx.xxx-xx!')
        if validar_idade(date_nascimento) > 110 or validar_idade(date_nascimento) < 0:
            return HttpResponse('Data de nascimento inválida!')
        if senha != confirma_senha:
            return HttpResponse('Senhas não conferem!')
        
        user = CustomUser.objects.create_user(username=criar_username(nome, cpf), nome=nome, cpf=cpf, date_nascimento=date_nascimento, grupo=grupo, covid_30_dias=covid_30_dias, password=senha, apto=apto)
        user.save()

        if user.apto:
            return HttpResponse('Usuário cadastrado com sucesso!')
        else:
            return HttpResponse('Usuário cadastrado com sucesso, porém não está apto para receber a vacina!')

@login_required(login_url='/login/')
def agendamento(request):
    return render(request, 'usuarios/agendamento.html')