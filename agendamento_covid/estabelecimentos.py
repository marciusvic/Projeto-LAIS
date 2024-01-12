import requests
import xml.etree.ElementTree as ET

class Estabelecimento:
    def __init__(self, co_unidade, co_cnes, no_razao_social, no_fantasia, no_logradouro, nu_endereco, no_complemento, no_bairro, co_cep, nu_telefone, nu_fax, no_email, nu_cnpj, co_atividade, co_clientela, nu_alvara, dt_expedicao, tp_orgao_expedidor, dt_val_lic_sani, tp_lic_sani, tp_unidade, co_turno_atendimento, co_estado_gestor, co_municipio_gestor, to_char_dt_atualizacao__dd_mm_yyyy___x, co_usuario_x, co_cpfdiretorcln, reg_diretorcln, st_adesao_filantrop, co_motivo_desab, no_url, nu_latitude, nu_longitude, to_char_dt_atu_geo__dd_mm_yyyy__, no_usuario_geo, co_natureza_jur, tp_estab_sempre_aberto, st_geracredito_gerente_sgif, st_conexao_internet, co_tipo_unidade_x, no_fantasia_abrev, tp_gestao, to_char_dt_atualizacao_origem__dd_mm_yyyy___x, co_tipo_estabelecimento, co_atividade_principal, st_contrato_formalizado, co_tipo_unidade_y, co_sub_tipo_unidade, to_char_dt_atualizacao__dd_mm_yyyy___y, co_usuario_y, to_char_dt_atualizacao_origem__dd_mm_yyyy___y):
        self.co_unidade = co_unidade
        self.co_cnes = co_cnes
        self.no_razao_social = no_razao_social
        self.no_fantasia = no_fantasia
        self.no_logradouro = no_logradouro
        self.nu_endereco = nu_endereco
        self.no_complemento = no_complemento
        self.no_bairro = no_bairro
        self.co_cep = co_cep
        self.nu_telefone = nu_telefone
        self.nu_fax = nu_fax
        self.no_email = no_email
        self.nu_cnpj = nu_cnpj
        self.co_atividade = co_atividade
        self.co_clientela = co_clientela
        self.nu_alvara = nu_alvara
        self.dt_expedicao = dt_expedicao
        self.tp_orgao_expedidor = tp_orgao_expedidor
        self.dt_val_lic_sani = dt_val_lic_sani
        self.tp_lic_sani = tp_lic_sani
        self.tp_unidade = tp_unidade
        self.co_turno_atendimento = co_turno_atendimento
        self.co_estado_gestor = co_estado_gestor
        self.co_municipio_gestor = co_municipio_gestor
        self.to_char_dt_atualizacao__dd_mm_yyyy___x = to_char_dt_atualizacao__dd_mm_yyyy___x
        self.co_usuario_x = co_usuario_x
        self.co_cpfdiretorcln = co_cpfdiretorcln
        self.reg_diretorcln = reg_diretorcln
        self.st_adesao_filantrop = st_adesao_filantrop
        self.co_motivo_desab = co_motivo_desab
        self.no_url = no_url
        self.nu_latitude = nu_latitude
        self.nu_longitude = nu_longitude
        self.to_char_dt_atu_geo__dd_mm_yyyy__ = to_char_dt_atu_geo__dd_mm_yyyy__
        self.no_usuario_geo = no_usuario_geo
        self.co_natureza_jur = co_natureza_jur
        self.tp_estab_sempre_aberto = tp_estab_sempre_aberto
        self.st_geracredito_gerente_sgif = st_geracredito_gerente_sgif
        self.st_conexao_internet = st_conexao_internet
        self.co_tipo_unidade_x = co_tipo_unidade_x
        self.no_fantasia_abrev = no_fantasia_abrev
        self.tp_gestao = tp_gestao
        self.to_char_dt_atualizacao_origem__dd_mm_yyyy___x = to_char_dt_atualizacao_origem__dd_mm_yyyy___x
        self.co_tipo_estabelecimento = co_tipo_estabelecimento
        self.co_atividade_principal = co_atividade_principal
        self.st_contrato_formalizado = st_contrato_formalizado
        self.co_tipo_unidade_y = co_tipo_unidade_y
        self.co_sub_tipo_unidade = co_sub_tipo_unidade
        self.to_char_dt_atualizacao__dd_mm_yyyy___y = to_char_dt_atualizacao__dd_mm_yyyy___y
        self.co_usuario_y = co_usuario_y
        self.to_char_dt_atualizacao_origem__dd_mm_yyyy___y = to_char_dt_atualizacao_origem__dd_mm_yyyy___y

def obter_estabelecimentos():
    url = "https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml"

    response = requests.get(url)

    estabelecimentos = []

    if response.status_code == 200:
        xml_content = response.content

        root = ET.fromstring(xml_content)

        for estabelecimento_elem in root.findall(".//estabelecimento"):
            co_unidade = estabelecimento_elem.find("co_unidade").text
            co_cnes = estabelecimento_elem.find("co_cnes").text
            no_razao_social = estabelecimento_elem.find("no_razao_social").text
            no_fantasia = estabelecimento_elem.find("no_fantasia").text
            no_logradouro = estabelecimento_elem.find("no_logradouro").text
            nu_endereco = estabelecimento_elem.find("nu_endereco").text
            no_complemento = estabelecimento_elem.find("no_complemento").text
            no_bairro = estabelecimento_elem.find("no_bairro").text
            co_cep = estabelecimento_elem.find("co_cep").text
            nu_telefone = estabelecimento_elem.find("nu_telefone").text
            nu_fax = estabelecimento_elem.find("nu_fax").text
            no_email = estabelecimento_elem.find("no_email").text
            nu_cnpj = estabelecimento_elem.find("nu_cnpj").text
            co_atividade = estabelecimento_elem.find("co_atividade").text
            co_clientela = estabelecimento_elem.find("co_clientela").text
            nu_alvara = estabelecimento_elem.find("nu_alvara").text
            dt_expedicao = estabelecimento_elem.find("dt_expedicao").text
            tp_orgao_expedidor = estabelecimento_elem.find("tp_orgao_expedidor").text
            dt_val_lic_sani = estabelecimento_elem.find("dt_val_lic_sani").text
            tp_lic_sani = estabelecimento_elem.find("tp_lic_sani").text
            tp_unidade = estabelecimento_elem.find("tp_unidade").text
            co_turno_atendimento = estabelecimento_elem.find("co_turno_atendimento").text
            co_estado_gestor = estabelecimento_elem.find("co_estado_gestor").text
            co_municipio_gestor = estabelecimento_elem.find("co_municipio_gestor").text
            to_char_dt_atualizacao__dd_mm_yyyy___x = estabelecimento_elem.find("to_char_dt_atualizacao__dd_mm_yyyy___x").text
            co_usuario_x = estabelecimento_elem.find("co_usuario_x").text
            co_cpfdiretorcln = estabelecimento_elem.find("co_cpfdiretorcln").text
            reg_diretorcln = estabelecimento_elem.find("reg_diretorcln").text
            st_adesao_filantrop = estabelecimento_elem.find("st_adesao_filantrop").text
            co_motivo_desab = estabelecimento_elem.find("co_motivo_desab").text
            no_url = estabelecimento_elem.find("no_url").text
            nu_latitude = estabelecimento_elem.find("nu_latitude").text
            nu_longitude = estabelecimento_elem.find("nu_longitude").text
            to_char_dt_atu_geo__dd_mm_yyyy__ = estabelecimento_elem.find("to_char_dt_atu_geo__dd_mm_yyyy__").text
            no_usuario_geo = estabelecimento_elem.find("no_usuario_geo").text
            co_natureza_jur = estabelecimento_elem.find("co_natureza_jur").text
            tp_estab_sempre_aberto = estabelecimento_elem.find("tp_estab_sempre_aberto").text
            st_geracredito_gerente_sgif = estabelecimento_elem.find("st_geracredito_gerente_sgif").text
            st_conexao_internet = estabelecimento_elem.find("st_conexao_internet").text
            co_tipo_unidade_x = estabelecimento_elem.find("co_tipo_unidade_x").text
            no_fantasia_abrev = estabelecimento_elem.find("no_fantasia_abrev").text
            tp_gestao = estabelecimento_elem.find("tp_gestao").text
            to_char_dt_atualizacao_origem__dd_mm_yyyy___x = estabelecimento_elem.find("to_char_dt_atualizacao_origem__dd_mm_yyyy___x").text
            co_tipo_estabelecimento = estabelecimento_elem.find("co_tipo_estabelecimento").text
            co_atividade_principal = estabelecimento_elem.find("co_atividade_principal").text
            st_contrato_formalizado = estabelecimento_elem.find("st_contrato_formalizado").text
            co_tipo_unidade_y = estabelecimento_elem.find("co_tipo_unidade_y").text
            co_sub_tipo_unidade = estabelecimento_elem.find("co_sub_tipo_unidade").text
            to_char_dt_atualizacao__dd_mm_yyyy___y = estabelecimento_elem.find("to_char_dt_atualizacao__dd_mm_yyyy___y").text
            co_usuario_y = estabelecimento_elem.find("co_usuario_y").text
            to_char_dt_atualizacao_origem__dd_mm_yyyy___y = estabelecimento_elem.find("to_char_dt_atualizacao_origem__dd_mm_yyyy___y").text

            estabelecimento_obj = Estabelecimento(
                co_unidade, co_cnes, no_razao_social, no_fantasia, no_logradouro, nu_endereco,
                no_complemento, no_bairro, co_cep, nu_telefone, nu_fax, no_email, nu_cnpj,
                co_atividade, co_clientela, nu_alvara, dt_expedicao, tp_orgao_expedidor,
                dt_val_lic_sani, tp_lic_sani, tp_unidade, co_turno_atendimento,
                co_estado_gestor, co_municipio_gestor, to_char_dt_atualizacao__dd_mm_yyyy___x,
                co_usuario_x, co_cpfdiretorcln, reg_diretorcln, st_adesao_filantrop,
                co_motivo_desab, no_url, nu_latitude, nu_longitude,
                to_char_dt_atu_geo__dd_mm_yyyy__, no_usuario_geo, co_natureza_jur,
                tp_estab_sempre_aberto, st_geracredito_gerente_sgif, st_conexao_internet,
                co_tipo_unidade_x, no_fantasia_abrev, tp_gestao,
                to_char_dt_atualizacao_origem__dd_mm_yyyy___x, co_tipo_estabelecimento,
                co_atividade_principal, st_contrato_formalizado, co_tipo_unidade_y,
                co_sub_tipo_unidade, to_char_dt_atualizacao__dd_mm_yyyy___y,
                co_usuario_y, to_char_dt_atualizacao_origem__dd_mm_yyyy___y)

            estabelecimentos.append(estabelecimento_obj)

    else:
        print("Falha ao obter o XML. Código de status:", response.status_code)

    return estabelecimentos

