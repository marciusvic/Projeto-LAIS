from django.shortcuts import render, redirect
from django.http import HttpResponse
from agendamento_covid.models import CustomUser, Agendamento
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from agendamento_covid.grupos import obter_grupos
from agendamento_covid.estabelecimentos import obter_estabelecimentos
from agendamento_covid.funcoes import validar_idade, validar_cpf_digitos, validar_cpf_tamanho, verificar_apto, criar_username, obter_estabelecimento_cod_unidade

def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/homeLogado.html', {'user_apto': request.user.apto})
    else:
        return render(request, 'usuarios/home.html')

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
    
def logout_view(request):
    logout(request)
    return redirect('/')

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
            error_message = 'CPF já cadastrado!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message})
        if not validar_cpf_tamanho(cpf):
            error_message = 'CPF inválido, você deve coloca-lo no formato xxx.xxx.xxx-xx!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message})
        if not validar_cpf_digitos(cpf):
            error_message = 'CPF inválido, o CPF deve ser composto apenas de números, no formato 00000000000!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message})
        if validar_idade(date_nascimento) > 110 or validar_idade(date_nascimento) < 0:
            error_message = 'Data de nascimento inválida!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message})
        if senha != confirma_senha:
            error_message = 'Senhas não conferem!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message})
        
        user = CustomUser.objects.create_user(username=criar_username(nome, cpf),
                                              nome=nome, cpf=cpf,
                                              date_nascimento=date_nascimento,
                                              grupo=grupo,
                                              covid_30_dias=covid_30_dias,
                                              password=senha,
                                              apto=apto)
        user.save()
        
        if user.apto:
            return HttpResponse('Usuário cadastrado com sucesso!')
        else:
            return HttpResponse('Usuário cadastrado com sucesso, porém não está apto para receber a vacina!')

@login_required(login_url='/')
def agendamento(request):
    if request.method == 'GET':
        estabelecimentos = obter_estabelecimentos()
        return render(request, 'usuarios/agendamento.html', {'estabelecimentos': estabelecimentos})
    else:
        estabelecimentos = obter_estabelecimentos()
        estabelecimentoCodUnidade = request.POST.get('estabelecimento')
        data = request.POST.get('data')
        return redirect('/agendamento/' + estabelecimentoCodUnidade + '/' + data + '/')


@login_required(login_url='/')
def selecionar_horario(request, cod_unidade=None, data=None):
    if request.method == 'GET':
        estabelecimentos = obter_estabelecimentos()
        estabelecimento = obter_estabelecimento_cod_unidade(estabelecimentos, cod_unidade)
        horarios = [5, 5, 5, 5, 5]
        vagas = Agendamento.objects.filter(data_agendamento=data, cod_unidade=cod_unidade)
        for vaga in vagas:
            hora_agendamento = vaga.hora_agendamento.strftime('%H:%M:%S')
            if hora_agendamento.startswith('13:00'):
                horarios[0] -= 1
            elif hora_agendamento.startswith('14:00'):
                horarios[1] -= 1
            elif hora_agendamento.startswith('15:00'):
                horarios[2] -= 1
            elif hora_agendamento.startswith('16:00'):
                horarios[3] -= 1
            elif hora_agendamento.startswith('17:00'):
                horarios[4] -= 1
        return render(request, 'usuarios/selecionar_horario.html', {'estabelecimento': estabelecimento, 'data': data, 'horarios': horarios})
    else:
        horario = request.POST.get('horario')
        usuarioAgendado = Agendamento.objects.filter(id_usuario=request.user.id, data_agendamento=data).exists()
        if usuarioAgendado:
            return HttpResponse('Usuário já possui agendamento para esta data!')
        
        
        agendamento = Agendamento.objects.create(id_usuario=request.user,
                                                 data_agendamento=data,
                                                 hora_agendamento=horario,
                                                 cod_unidade=cod_unidade)
        agendamento.save()

        return redirect('/')
