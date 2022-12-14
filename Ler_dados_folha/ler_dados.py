
from openpyxl import load_workbook
import os

DADOS_LIDOS_FOLHA = './temp/dados_lidos_folha.txt'
DATA_ARQUIVO_FOLHA = './temp/data_arquivo_folha.txt'


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


def ler_dados_folha_auxiliar(plan_folha):

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

    dicionario_empresas = {}
    data = False

    for linha_folha in planilha_nova:

        # limpar strings vazias '' e NoneTypes

        # pegar empresa
        if not not linha_folha:
            if len(linha_folha[0]) >= 8:
                if linha_folha[0][0:7] == 'Empresa':
                    if not dicionario_empresas.get(linha_folha[0]):
                        dicionario_empresas[linha_folha[0]] = {}
                        empresa = linha_folha[0]

            if len(linha_folha[0]) >= 7 and not data:

                if linha_folha[0][0:7] == 'Espelho':

                    if 'COMPLEMENTAR' in linha_folha[0].upper().split(' '):
                        data = True
                        with open(DATA_ARQUIVO_FOLHA, 'a', encoding='ansi') as data:
                            print(linha_folha[0][59::].split(
                                ' ')[0], file=data)
                    elif 'ADIANTAMENTO' in linha_folha[0].upper().split(' '):
                        data = True
                        with open(DATA_ARQUIVO_FOLHA, 'a', encoding='ansi') as data:
                            print(linha_folha[0].split(
                                ' ')[-1], file=data)
                    else:
                        data = True
                        with open(DATA_ARQUIVO_FOLHA, 'a', encoding='ansi') as data:
                            print(linha_folha[0][53::], file=data)

            if len(linha_folha[0]) >= 17:
                if linha_folha[0][0:17] == 'Centro de Custo :':
                    if not dicionario_empresas[empresa].get(linha_folha[1]):
                        dicionario_empresas[empresa][linha_folha[1]] = {
                        }
                        centro_de_custo = linha_folha[1]
                        Rota.centro_custo = True


            if len(linha_folha) == 3:
                if not not linha_folha[0]:
                    if eh_numero(linha_folha[0]) and Rota.centro_custo:
                        dicionario_empresas[empresa][centro_de_custo][linha_folha[0]
                                                                    ] = [linha_folha[1], linha_folha[2]]
            elif len(linha_folha) == 4:
                if type(linha_folha[2]) is str:
                    if not not linha_folha[0]:
                        if eh_numero(linha_folha[0]) and Rota.centro_custo:
                            dicionario_empresas[empresa][centro_de_custo][linha_folha[0]
                                                                        ] = [linha_folha[1], linha_folha[3]]

            elif len(linha_folha) == 6:
                if not not linha_folha[0]:
                    if eh_numero(linha_folha[0]) and Rota.centro_custo:
                        dicionario_empresas[empresa][centro_de_custo][linha_folha[0]
                                                                    ] = [linha_folha[1], linha_folha[2]]
                if not not linha_folha[3]:
                    if eh_numero(linha_folha[3]) and eh_numero(linha_folha[0]) and Rota.centro_custo:
                        dicionario_empresas[empresa][centro_de_custo][linha_folha[3]
                                                                    ] = [linha_folha[4], linha_folha[5]]
            elif len(linha_folha) == 7:
            
                if type(linha_folha[2]) is str:
                    if not not linha_folha[0]:
                        if eh_numero(linha_folha[0]) and Rota.centro_custo:
                            dicionario_empresas[empresa][centro_de_custo][linha_folha[0]
                                                                        ] = [linha_folha[1], linha_folha[3]]
                    if not not linha_folha[4]:
                        if eh_numero(linha_folha[4]) and eh_numero(linha_folha[0]) and Rota.centro_custo:
                            dicionario_empresas[empresa][centro_de_custo][linha_folha[4]
                                                                        ] = [linha_folha[5], linha_folha[6]]
                else:

                    if not not linha_folha[0]:
                        if eh_numero(linha_folha[0]) and Rota.centro_custo:
                            dicionario_empresas[empresa][centro_de_custo][linha_folha[0]
                                                                        ] = [linha_folha[1], linha_folha[2]]
                    if not not linha_folha[3]:
                        if eh_numero(linha_folha[3]) and eh_numero(linha_folha[0]) and Rota.centro_custo:
                            dicionario_empresas[empresa][centro_de_custo][linha_folha[3]
                                                                        ] = [linha_folha[4], linha_folha[6]]
            elif len(linha_folha) == 8:
                if type(linha_folha[2]) is str or type(linha_folha[6]) is str:
                     if not not linha_folha[0] and not not linha_folha[4]:
                        if eh_numero(linha_folha[0]) and Rota.centro_custo:
                            dicionario_empresas[empresa][centro_de_custo][linha_folha[0]
                                                                        ] = [linha_folha[1], linha_folha[3]]
                        if eh_numero(linha_folha[4]) and Rota.centro_custo:
                            dicionario_empresas[empresa][centro_de_custo][linha_folha[4]
                                                                        ] = [linha_folha[5], linha_folha[7]]





            if not not linha_folha[0]:
                if linha_folha[0] == 'Total FGTS' and Rota.centro_custo:
                    dicionario_empresas[empresa][centro_de_custo]['FGTS'] = [
                        'FGTS', linha_folha[1]]

            if not not linha_folha[0]:
                if linha_folha[0] == 'GPS patronal - >' and Rota.centro_custo:
                    dicionario_empresas[empresa][centro_de_custo]['GPS_PATRONAL'] = [
                        'GPS_PATRONAL', linha_folha[2].split(' ')[0]]
                    Rota.centro_custo = False
                    Rota.resumo_geral = False
                    Rota.total_fgts = False
                    Rota.GPS_patronal = False

    return dicionario_empresas


def ler_folha_completa(plan_folha):

    remover_arquivo(DADOS_LIDOS_FOLHA)
    remover_arquivo(DATA_ARQUIVO_FOLHA)

    dicionario_empresa = ler_dados_folha_auxiliar(
         plan_folha)

    return dicionario_empresa
