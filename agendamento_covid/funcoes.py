from datetime import datetime

def validar_idade(data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    data_atual = datetime.now()
    diferenca = data_atual - data_nascimento
    idade = diferenca.days // 365

    return idade

def validar_cpf_digitos(cpf):
    return cpf.isdigit()

def validar_cpf_tamanho(cpf):
    return len(cpf) == 11

def verificar_apto(grupo, covid, idade):
    if grupo == 'População Privada de Liberdade' or grupo == 'Pessoas com Deficiência Institucionalizadas' or grupo == 'ACAMADAS de 80 anos ou mais' or covid == True or idade < 18:
        return False
    else:
        return True

def criar_username(nome, cpf):
    nome = nome.split()[0]
    username = nome + cpf
    return username

def obter_estabelecimento_cod_unidade(estabelecimentos, estabelecimentoCodUnidade):
    estabelecimento = None
    for estab in estabelecimentos:
        if int(estab.co_unidade) == int(estabelecimentoCodUnidade):
            estabelecimento = estab
            return estabelecimento
    return estabelecimento
