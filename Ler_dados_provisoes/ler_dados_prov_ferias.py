
from openpyxl import load_workbook
import os
from converter_valores import converter as converte

DADOS_LIDOS_FOLHA = './temp/dados_lidos_folha_prov_ferias_ant.txt'
DATA_ARQUIVO_FOLHA = './temp/data_arquivo_prov_ferias.txt'


class Rota:
    centro_custo = False
    resumo_geral = False
    total_fgts = False
    GPS_patronal = False


def eh_numero(valor):
    try:
        val = int(valor)
        return True
    except ValueError:
        return False


def remover_arquivo(arquivo):
    if os.path.exists(arquivo):
        os.remove(arquivo)


def existe_arquivo(arquivo):
    if os.path.exists(arquivo):
        return True
    return False


def ler_dados_folha_prov_anter_ferias(plan_folha):

  # ler layout folha
    planilha_nova = []
    for linha in plan_folha.values:
        nova_lista = []
        for lista_velha in linha:
            if lista_velha:
                nova_lista.append(lista_velha)
        planilha_nova.append(nova_lista)

    dicionario_empresas = {}
    data = False

    for linha_folha in planilha_nova:

        # limpar strings vazias '' e NoneTypes

        # pegar empresa
        if linha_folha:
            if len(linha_folha[0]) >= 8:
                if linha_folha[0][0:7] == 'Empresa':
                    if not dicionario_empresas.get(linha_folha[0]):
                        dicionario_empresas[linha_folha[0]] = {}
                        empresa = linha_folha[0]

            if len(linha_folha[0]) >= 9 and not data:
                if linha_folha[0][0:9].upper() == 'RELATÓRIO':
                    data = True
                    with open(DATA_ARQUIVO_FOLHA, 'a', encoding='ansi') as data:
                        print(linha_folha[0][32:40], file=data)

            if len(linha_folha[0]) >= 22:
                if linha_folha[0][0:21] == 'TOTAL CENTRO DE CUSTO':
                    centro_de_custo = linha_folha[0][24::]
                    # print(centro_de_custo)
                    if not dicionario_empresas[empresa].get(centro_de_custo):
                        dicionario_empresas[empresa][centro_de_custo] = {
                        }
                        Rota.centro_custo = True

        # verificar se é um valor valido na coluna do total_saldo
        if linha_folha:
            if linha_folha[0] == 'Total saldo:' and Rota.centro_custo:

                dicionario_empresas[empresa][centro_de_custo]['PROVFERIAS'
                                                              ] = converte.converte_valor_float(linha_folha[1],
                                                                                                linha_folha[2])

                dicionario_empresas[empresa][centro_de_custo]['PROVFGTSFERIAS'
                                                              ] = converte.converte_valor_float(linha_folha[3])
                dicionario_empresas[empresa][centro_de_custo]['PROVINSSFERIAS'
                                                              ] = converte.converte_valor_float(linha_folha[4],
                                                                                                linha_folha[5], linha_folha[6])

                Rota.centro_custo = False

    return dicionario_empresas


def ler_folha_provisao_ferias(plan_prov_13):

    remover_arquivo(DADOS_LIDOS_FOLHA)
    remover_arquivo(DATA_ARQUIVO_FOLHA)

    dic_prov = ler_dados_folha_prov_anter_ferias(
        plan_prov_13)

    return dic_prov
