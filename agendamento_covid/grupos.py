import requests
import xml.etree.ElementTree as ET

class Grupo:
    def __init__(self, nome, visivel, fase, codigo_si_pni, grupo_pai, criado_em, atualizado_em):
        self.nome = nome
        self.visivel = visivel
        self.fase = fase
        self.codigo_si_pni = codigo_si_pni
        self.grupo_pai = grupo_pai
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

def obter_grupos():
    url = "https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml"

    response = requests.get(url)

    grupos = []

    if response.status_code == 200:
        xml_content = response.content

        root = ET.fromstring(xml_content)

        for grupo_elem in root.findall(".//grupoatendimento"):
            nome = grupo_elem.find("nome").text
            visivel = grupo_elem.find("visivel").text
            fase = grupo_elem.find("fase").text
            codigo_si_pni = grupo_elem.find("codigo_si_pni").text
            grupo_pai = grupo_elem.find("grupo_pai").text
            criado_em = grupo_elem.find("criado_em").text
            atualizado_em = grupo_elem.find("atualizado_em").text

            grupo_obj = Grupo(nome, visivel, fase, codigo_si_pni, grupo_pai, criado_em, atualizado_em)

            grupos.append(grupo_obj)

    else:
        print("Falha ao obter o XML. Código de status:", response.status_code)

    return grupos
