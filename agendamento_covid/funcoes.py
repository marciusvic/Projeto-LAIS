from datetime import datetime

def validar_idade(data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    data_atual = datetime.now()
    diferenca = data_atual - data_nascimento
    idade = diferenca.days // 365

    return idade

def validar_cpf(cpf):
    cpf = cpf.replace('.', '').replace('-', '')
    if not cpf.isnumeric():
        return False
    else:
        return True