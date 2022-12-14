
from datas import calcular_datas as datas
from layout_saida_folha import folha_layout_saida as gera_layout_fopag
import os


def remover_arquivo(arquivo):
    if os.path.exists(arquivo):
        os.remove(arquivo)


def processar_folha(dados_lidos_folha, dic_nome_empresas,
                    dic_nome_centro_custos, dic_eventos, sistema):
    teve_erros = False

    data = datas.ler_data('./temp/data_arquivo_folha.txt')

    nao_eh_custo = ['EVENTO', 'DESCRICAO', 'CREDITO',
                    'HIST', 'PROVENTO', 'TIPO', 'SERVICOS']
    dic_custos = {}

    matriz = False
    filial = False
    imprimir = False
    log_lista = []

    with open('./arquivo_gerado/log_folha.txt', 'a', encoding='ansi') as log:
        with open('./arquivo_gerado/arquivo_importacao_folha.txt', 'a', encoding='ansi') as saida:
            for empresa, restante in dados_lidos_folha.items():
                if dic_nome_empresas.get(empresa):
                    codigo_empresa = str(dic_nome_empresas.get(
                        empresa)[1])
                else:
                    print(f'empresa {empresa} nao encontrada :(', file=log)
                    teve_erros = True
                    continue

                for centro_custo, restante_2 in restante.items():

                    if sistema == 'Allianza-Imex' or sistema == 'SB-Rubenich' or sistema == 'Super-Safra':
                        # print(dic_nome_centro_custos)
                        if dic_nome_centro_custos.get(centro_custo):
                            codigo_centro_custo = str(dic_nome_centro_custos.get(centro_custo)[
                                1])
                        else:
                            print(f'centro de custos {centro_custo} nao encontrado :(', file=log)
                            teve_erros = True
                            continue

                    for eventos, restante_3 in restante_2.items():
                        if sistema == 'Allianza-Imex' or sistema == 'MPE' or sistema == 'SB-Rubenich' \
                                or sistema == 'Camsul' or sistema == 'Super-Safra':
                            if dic_eventos.get(eventos):
                                descricao = str(dic_eventos.get(eventos)[1])
                                debito = str(dic_eventos.get(eventos)[2])
                                credito = str(dic_eventos.get(eventos)[3])
                                hist = str(dic_eventos.get(eventos)[4])
                                valor = restante_3[1]
                                imprimir = True
                            else:
                                if eventos not in log_lista:
                                    log_lista.append(eventos)
                                    print(f'evento {eventos} nao encontrado :(', file=log)
                                    teve_erros = True
                                    continue
                        elif sistema == 'DELLA-PASQUA':

                            if centro_custo[0:3] == '162':
                                matriz = True
                                indice = 4
                            elif empresa.split(' ')[1] == '184':
                                filial = True
                                indice = 5
                            else:
                                indice = 6
                            if dic_eventos.get(eventos):
                                descricao = str(
                                    dic_eventos.get(eventos)[1])
                                if dic_eventos.get(eventos)[7] == 'PROVENTO':
                                    debito = str(
                                        dic_eventos.get(eventos)[indice])
                                    credito = str(
                                        dic_eventos.get(eventos)[3])
                                else:
                                    credito = str(
                                        dic_eventos.get(eventos)[indice])
                                    debito = str(
                                        dic_eventos.get(eventos)[3])

                                hist = str(dic_eventos.get(eventos)[2])
                                valor = restante_3[1]

                            else:
                                if eventos not in log_lista:
                                    log_lista.append(eventos)
                                    print(f'evento {eventos} não encontrado :(', file=log)
                                    teve_erros = True
                                    continue

                        elif sistema == 'MULTI':
                            if dic_eventos.get(eventos):
                                descricao = str(dic_eventos.get(eventos)[1])
                                valor = restante_3[1]

                                if centro_custo in dic_eventos.get('Evento'):

                                    lista = dic_eventos.get('Evento')

                                    debito = str(
                                        dic_eventos.get(eventos)[lista.index(centro_custo)])
                                    credito = str(
                                        dic_eventos.get(eventos)[2])
                                else:
                                    print(
                                        f'centro de custos {centro_custo} não encontrado :(', file=log)
                                    teve_erros = True
                                    continue

                            else:
                                if eventos not in log_lista:
                                    log_lista.append(eventos)
                                    print(f'evento {eventos} não encontrado :(', file=log)
                                    teve_erros = True
                                    continue
                        
                        elif sistema == 'Cootranscau':
                            if dic_eventos.get(eventos):
                                descricao = str(dic_eventos.get(eventos)[1])
                                valor = restante_3[1]

                                if centro_custo in dic_eventos.get('Evento'):

                                    lista = dic_eventos.get('Evento')

                                    if (dic_eventos.get(eventos)[2]).upper() == 'P':

                                        debito = str(
                                            dic_eventos.get(eventos)[lista.index(centro_custo)])
                                        credito = str(
                                            dic_eventos.get(eventos)[3])
                                    else:
                                        credito = str(
                                            dic_eventos.get(eventos)[lista.index(centro_custo)])
                                        debito = str(
                                            dic_eventos.get(eventos)[3])
                                    hist = dic_eventos.get(eventos)[1]

                                else:
                                    if centro_custo not in log_lista:
                                        log_lista.append(centro_custo)
                                        print(
                                            f'centro de custos {centro_custo} não encontrado :(', file=log)
                                        teve_erros = True
                                        continue

                            else:
                                if eventos not in log_lista:
                                    log_lista.append(eventos)
                                    print(f'evento {eventos} não encontrado :(', file=log)
                                    teve_erros = True
                                    continue

                        if dic_eventos.get(eventos):
                            if sistema == 'Allianza-Imex' or sistema == 'SB-Rubenich' or sistema == 'Super-Safra':
                                gera_layout_fopag.ImexAllianza(codigo_empresa, data, debito,
                                                            codigo_centro_custo,
                                                            credito, hist, descricao, saida, valor)
                            elif sistema == 'MPE' and imprimir:
                                gera_layout_fopag.MPE(codigo_empresa, data, debito,
                                                    credito, hist, descricao, saida, valor)
                                imprimir = False
                            elif sistema == 'DELLA-PASQUA':
                                gera_layout_fopag.DELLA_PASQUA(codigo_empresa, data, debito,
                                                            credito, hist, descricao, saida, valor)
                            elif sistema == 'MULTI':
                                gera_layout_fopag.Multi(codigo_empresa, data, debito,
                                                        credito, descricao, valor, centro_custo)
                            elif sistema == 'Camsul':
                                gera_layout_fopag.Camsul(codigo_empresa, data, debito,
                                                        credito, descricao, valor, centro_custo)
                            elif sistema == 'Cootranscau':
                                gera_layout_fopag.Cootranscau(codigo_empresa, data, debito,
                                    
                                                            credito, descricao, saida, valor, hist, centro_custo)
        if sistema == 'DELLA-PASQUA':
            if not matriz or not filial:
                print(
                    'nao encontrou centro de custos para matriz ou filial, pode haver erro de contas nos lançamentos destas', file=log)
                teve_erros = True
        if sistema == 'MULTI' or sistema == 'Camsul':
            remover_arquivo('./arquivo_gerado/arquivo_importacao_folha.txt')

        if not teve_erros:
            print('Folha gerada com sucesso \o/\o/', file=log)
