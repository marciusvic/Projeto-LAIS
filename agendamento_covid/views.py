from django.shortcuts import render, redirect
from django.http import HttpResponse
from agendamento_covid.models import CustomUser, Agendamento
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from datetime import datetime
from agendamento_covid.grupos import obter_grupos
from agendamento_covid.estabelecimentos import obter_estabelecimentos
from agendamento_covid.funcoes import validar_idade, validar_cpf_digitos, validar_cpf_tamanho, verificar_apto, criar_username, obter_estabelecimento_cod_unidade
from django.utils import timezone

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
    grupos = obter_grupos()
    if request.method == 'GET':
        return render(request, 'usuarios/cadastrar.html', {'grupos': grupos})
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
        else:
            apto = False

        cpf = request.POST.get('cpf')
        cpf_existe = CustomUser.objects.filter(cpf=cpf).exists()
        if cpf_existe:
            error_message = 'CPF já cadastrado!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message, 'grupos': grupos})
        if not validar_cpf_tamanho(cpf):
            error_message = 'CPF inválido, você deve coloca-lo no formato xxx.xxx.xxx-xx!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message, 'grupos': grupos})
        if not validar_cpf_digitos(cpf):
            error_message = 'CPF inválido, o CPF deve ser composto apenas de números, no formato 00000000000!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message, 'grupos': grupos})
        if validar_idade(date_nascimento) > 110 or validar_idade(date_nascimento) < 0:
            error_message = 'Data de nascimento inválida!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message, 'grupos': grupos})
        if senha != confirma_senha:
            error_message = 'Senhas não conferem!'
            return render(request, 'usuarios/cadastrar.html', {'error_message': error_message, 'grupos': grupos})
        
        user = CustomUser.objects.create_user(username=criar_username(nome, cpf),
                                              nome=nome, cpf=cpf,
                                              date_nascimento=date_nascimento,
                                              grupo=grupo,
                                              covid_30_dias=covid_30_dias,
                                              password=senha,
                                              apto=apto)
        user.save()
        
        if user.apto == True:
            return render(request, 'usuarios/login.html', {'success_message': 'Usuário cadastrado com sucesso!'})
        else:
            return render(request, 'usuarios/login.html', {'success_message': 'Usuário cadastrado com sucesso, porém não está apto para receber a vacina!'})

@login_required(login_url='/')
def agendamento(request):
    estabelecimentos = obter_estabelecimentos()
    if request.method == 'GET':
        return render(request, 'usuarios/agendamento.html', {'estabelecimentos': estabelecimentos})
    else:
        if request.POST.get('estabelecimento') == '':
            return render(request, 'usuarios/agendamento.html', {'error_message': 'Selecione um estabelecimento!', 'estabelecimentos': estabelecimentos})
        if request.POST.get('data') == None:
            return render(request, 'usuarios/agendamento.html', {'error_message': 'Selecione uma data!', 'estabelecimentos': estabelecimentos})
        if request.POST.get('data') <= str(datetime.today().date()):
            return render(request, 'usuarios/agendamento.html', {'error_message': 'Agendamentos só podem ser realizados para datas futuras. Selecione uma data válida!', 'estabelecimentos': estabelecimentos})
        data_agendamento = datetime.strptime(request.POST.get('data'), '%Y-%m-%d').date()
        if not (1 < data_agendamento.weekday() < 6):
            return render(request, 'usuarios/agendamento.html', {'error_message': 'Agendamentos só podem ser realizados de quarta-feira a sábado. Selecione uma data válida!', 'estabelecimentos': estabelecimentos})
        estabelecimentos = obter_estabelecimentos()
        estabelecimentoCodUnidade = request.POST.get('estabelecimento')
        data = request.POST.get('data')
        return redirect('/agendamento/' + estabelecimentoCodUnidade + '/' + data + '/')


@login_required(login_url='/')
def selecionar_horario(request, cod_unidade=None, data=None):
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
    if request.method == 'GET':
        return render(request, 'usuarios/selecionar_horario.html', {'estabelecimento': estabelecimento, 'data': data, 'horarios': horarios})
    else:
        horario = request.POST.get('horario')
        usuarioAgendado = Agendamento.objects.filter(id_usuario=request.user.id,
                                                     data_agendamento=data).exists()
        
        Agendamentos = Agendamento.objects.filter(data_agendamento=data,
                                                  cod_unidade=cod_unidade,
                                                  hora_agendamento=horario).count()
        idade = validar_idade(str(request.user.date_nascimento))
        if usuarioAgendado:
            return render(request, 'usuarios/agendamento.html', {'error_message': 'Você já possui um agendamento para esta data, cada pessoa só pode ter um agendamento por vez!', 'estabelecimentos': estabelecimentos})
        if Agendamentos >= 5:
            return render(request, 'usuarios/agendamento.html', {'error_message': 'Horário indisponível, selecione outro horário!', 'estabelecimentos': estabelecimentos})
        if horario == None:
            return render(request, 'usuarios/selecionar_horario.html', {'error_message': 'Selecione um horário!', 'estabelecimento': estabelecimento, 'data': data, 'horarios': horarios})
        
        if (idade <= 17 or idade >= 30) and str(horario) == '13:00':
            return render(request, 'usuarios/selecionar_horario.html', {'error_message': 'Horário indisponível para sua idade, o horário das 13:00 só está disponível para pessoas entre 18 a 29 anos', 'estabelecimento': estabelecimento, 'data': data, 'horarios': horarios})
        if (idade <= 29 or idade >= 40) and str(horario) == '14:00':
            return render(request, 'usuarios/selecionar_horario.html', {'error_message': 'Horário indisponível para sua idade, o horário das 14:00 só está disponível para pessoas entre 30 a 39 anos', 'estabelecimento': estabelecimento, 'data': data, 'horarios': horarios})
        if (idade <= 39 or idade >= 50) and str(horario) == '15:00':
            return render(request, 'usuarios/selecionar_horario.html', {'error_message': 'Horário indisponível para sua idade, o horário das 15:00 só está disponível para pessoas entre 40 a 49 anos', 'estabelecimento': estabelecimento, 'data': data, 'horarios': horarios})
        if (idade <= 49 or idade >= 60) and str(horario) == '16:00':
            return render(request, 'usuarios/selecionar_horario.html', {'error_message': 'Horário indisponível para sua idade, o horário das 16:00 só está disponível para pessoas entre 50 a 59 anos', 'estabelecimento': estabelecimento, 'data': data, 'horarios': horarios})
        if idade > 59 and str(horario) == '17:00':
            return render(request, 'usuarios/selecionar_horario.html', {'error_message': 'Horário indisponível para sua idade, o horário das 17:00 só está disponível para pessoas com 60 anos ou mais', 'estabelecimento': estabelecimento, 'data': data, 'horarios': horarios})
        
        agendamento = Agendamento.objects.create(id_usuario=request.user,
                                                 data_agendamento=data,
                                                 hora_agendamento=horario,
                                                 cod_unidade=cod_unidade)
        agendamento.save()
        return redirect('/')
    
@login_required(login_url='/')
def listar_agendamentos(request):
    estabelecimentos = obter_estabelecimentos()
    agendamentos = Agendamento.objects.filter(id_usuario=request.user.id)
    infos_agendamentos = []
    for agendamento in agendamentos:
        data_agendamento = agendamento.data_agendamento
        hora_agendamento = agendamento.hora_agendamento

        agora = timezone.now().astimezone().replace(microsecond=0)
        
        if data_agendamento > agora.date() or (data_agendamento == agora.date() and hora_agendamento > agora.time()):
            infos_agendamentos.append({
                'data': data_agendamento.strftime('%Y-%m-%d'),
                'hora': hora_agendamento.strftime('%H:%M:%S'),
                'estabelecimento': obter_estabelecimento_cod_unidade(estabelecimentos, agendamento.cod_unidade),
                'ja_realizado': False
            })
        else:
            infos_agendamentos.append({
                'data': data_agendamento.strftime('%Y-%m-%d'),
                'hora': hora_agendamento.strftime('%H:%M:%S'), 
                'estabelecimento': obter_estabelecimento_cod_unidade(estabelecimentos, agendamento.cod_unidade),
                'dia_semana': data_agendamento.strftime('%A'),
                'ja_realizado': True
            })

    return render(request, 'usuarios/listar_agendamentos.html', {'infos_agendamentos': infos_agendamentos})

