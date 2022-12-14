
from datas import calcular_datas as calcular
from converter_valores import converter
from layout_saida_folha import folha_layout_saida as gera_layout_provisoes
from remocao_arquivos.remover import remover_arquivo


def calcular_saldo_provisoes(valor_prov_2, dados_lidos_1, empresa, centro_custo, eventos):

    if dados_lidos_1.get(empresa):
        if dados_lidos_1[empresa].get(centro_custo):
            if dados_lidos_1[empresa][centro_custo].get(eventos):
                saldo = valor_prov_2 - \
                    (dados_lidos_1[empresa][centro_custo].get(eventos))
            else:
                saldo = valor_prov_2
        else:
            saldo = valor_prov_2
    else:
        saldo = valor_prov_2

    saldo = round(saldo, 2)
    return saldo


def processar_provisao(dados_lidos_prov_13_1, dados_lidos_prov_13_2, dic_nome_empresas,
                       dic_nome_centro_custos, dic_eventos, sistema, path_data, DECIMO):
    teve_erros = False

    matriz = False
    filial = False
    data = calcular.ler_data(path_data)

    with open('./arquivo_gerado/log_folha.txt', 'a', encoding='ansi') as log:
        with open('./arquivo_gerado/arquivo_importacao_folha.txt', 'a', encoding='ansi') as saida:
            for empresa, restante in dados_lidos_prov_13_2.items():

                if dic_nome_empresas.get(empresa):
                    codigo_empresa = str(dic_nome_empresas.get(
                        empresa)[1])
                else:
                    print(f'{empresa} não encontrado :(', file=log)
                    teve_erros = True
                    continue

                for centro_custo, restante_2 in restante.items():

                    if sistema == 'Allianza-Imex' or sistema == 'SB-Rubenich' or sistema == 'Super-Safra':

                        if dic_nome_centro_custos.get(centro_custo):
                            codigo_centro_custo = str(dic_nome_centro_custos.get(centro_custo)[
                                1])
                        else:
                            print(f'{centro_custo} não encontrado :(', file=log)
                            teve_erros = True
                            continue

                    for eventos, restante_3 in restante_2.items():
                        if sistema == 'Allianza-Imex' or sistema == 'MPE' or sistema == 'SB-Rubenich' or \
                                sistema == 'Camsul' or sistema == 'Super-Safra':
                            if dic_eventos.get(eventos):

                                descricao = str(dic_eventos.get(eventos)[1])
                                debito = str(dic_eventos.get(eventos)[2])
                                credito = str(dic_eventos.get(eventos)[3])
                                hist = str(dic_eventos.get(eventos)[4])
                                valor = calcular_saldo_provisoes(restante_3,
                                                                 dados_lidos_prov_13_1, empresa,
                                                                 centro_custo, eventos)
                                if valor < 0:
                                    (debito, credito) = (credito, debito)
                                    valor = valor * -1
                                valor = converter.converte_valor_string(valor)

                            else:
                                print(f'{eventos} não encontrado :(', file=log)
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

                                valor = calcular_saldo_provisoes(restante_3,
                                                                 dados_lidos_prov_13_1, empresa,
                                                                 centro_custo, eventos)
                                if valor < 0:
                                    (debito, credito) = (credito, debito)
                                    valor = valor * -1
                                valor = converter.converte_valor_string(valor)
                            else:
                                print(f'{eventos} não encontrado :(', file=log)
                                teve_erros = True
                                continue
                        elif sistema == 'MULTI':

                            if dic_eventos.get(eventos):

                                if centro_custo in dic_eventos.get('Evento'):

                                    descricao = str(
                                        dic_eventos.get(eventos)[1])
                                    lista = dic_eventos.get('Evento')

                                    debito = str(
                                        dic_eventos.get(eventos)[lista.index(centro_custo)])
                                    credito = str(
                                        dic_eventos.get(eventos)[2])

                                    valor = calcular_saldo_provisoes(restante_3,
                                                                     dados_lidos_prov_13_1, empresa,
                                                                     centro_custo, eventos)
                                    if valor < 0:
                                        (debito, credito) = (credito, debito)
                                        valor = valor * -1
                                    valor = converter.converte_valor_string_separacao_ponto(
                                        valor)

                                else:
                                    print(
                                        f'{centro_custo} não encontrado :(', file=log)
                                    teve_erros = True
                                    continue

                            else:

                                print(f'{eventos} não encontrado :(', file=log)
                                teve_erros = True
                                continue

                        if sistema == 'Allianza-Imex' or sistema == 'SB-Rubenich' or sistema == 'Super-Safra':
                            gera_layout_provisoes.ImexAllianza(codigo_empresa, data, debito,
                                                               codigo_centro_custo,
                                                               credito, hist, descricao, saida, valor)
                        elif sistema == 'MPE':
                            gera_layout_provisoes.MPE(codigo_empresa, data, debito,
                                                      credito, hist, descricao, saida, valor)
                        elif sistema == 'DELLA-PASQUA':
                            gera_layout_provisoes.DELLA_PASQUA(codigo_empresa, data, debito,
                                                               credito, hist, descricao, saida, valor)
                        elif sistema == 'MULTI':
                            gera_layout_provisoes.Multi(codigo_empresa, data, debito,
                                                        credito, descricao, valor, centro_custo, True)
                        elif sistema == 'Camsul':
                            gera_layout_provisoes.Camsul(codigo_empresa, data, debito,
                                                         credito, descricao, valor, centro_custo, True)

        if sistema == 'DELLA-PASQUA':
            if not matriz or not filial:
                print(
                    'nao encontrou centro de custos para matriz ou filial, pode haver erro de contas nos lançamentos destas nas provisoes', file=log)
                teve_erros = True
        if sistema == 'MULTI' or sistema == 'Camsul':
            remover_arquivo('./arquivo_gerado/arquivo_importacao_folha.txt')

        if not teve_erros and DECIMO:
            print('Provisao_13_salario gerada com sucesso \o/\o/', file=log)
        elif not teve_erros and not DECIMO:
            print('Provisao_Ferias gerada com sucesso \o/\o/', file=log)
