from converter_valores import converter as converte


def ImexAllianza(codigo_empresa, data, debito, codigo_centro_custo,
                 credito, hist, descricao, saida, valor):

    valor = converte.converte_valor_string(valor)

    # print(type(debito), debito)
    if debito != 'None' and credito != 'None' and valor != '0,0':
        lancamento = codigo_empresa + '|' + data + '|' + debito + \
            '|' + codigo_centro_custo + '|' \
            + credito + '|' + codigo_centro_custo + '|' \
            + hist + '|' + descricao + '|' \
            + valor + '|' + ';'

        print(lancamento, file=saida)

def Cootranscau(codigo_empresa, data, debito,
                        credito, descricao, saida, valor, hist, centro_custo):

  
    valor = converte.ajustar_casas_1_dezena_valor(valor)
    valor = valor.replace('.', '').replace(',', '').strip().zfill(13)

    # valor = valor.zfill(13)

    hist = hist + ' ' + data[3::] + ' ' + centro_custo
    hist = 'VLR.REF.' + hist
    hist = hist.ljust(160)

    # print(type(debito), debito)
    if debito != 'None' and credito != 'None' and valor != '0,0':
        debito = debito.zfill(7)
        credito = credito.zfill(7)
        credito = credito.ljust(29)
        lancamento = '0'.zfill(13) + data + data + debito + '0'.zfill(4) + 'D' + valor + hist + credito + '001'
        print(lancamento, file=saida)

def Multi(codigo_empresa, data, debito,
          credito, descricao, valor, centro_custo, PROVISAO=False):

    sep = ','

    valor = converte.converte_valor_string_separacao_ponto(valor)

    descricao = descricao + ' ' + data[3::]

    data = data.replace('/', '')

    lancamento = codigo_empresa + sep + data + sep + \
        debito + sep + \
        credito + sep + \
        valor + sep + '' + sep + descricao + sep + '' + sep

    with open('./arquivo_gerado/' + centro_custo + '.fpa', 'a', encoding='utf-8') as saida:
        print(lancamento, file=saida)


def Camsul(codigo_empresa, data, debito,
           credito, descricao, valor, centro_custo, PROVISAO=False):

    sep = ','

    valor = converte.converte_valor_string_separacao_ponto(valor)

    descricao = descricao + ' ' + data[3::]

    data = data.replace('/', '')

    if debito != 'None' and credito != 'None' and valor != '0,0':
        lancamento = codigo_empresa + sep + data + sep + \
            debito + sep + \
            credito + sep + \
            valor + sep + '' + sep + descricao + sep + '' + sep

        with open('./arquivo_gerado/' + 'arquivo_importacao_folha.txt' + '.fpa', 'a', encoding='utf-8') as saida:
            print(lancamento, file=saida)


def MPE(codigo_empresa, data, debito,
        credito, hist, descricao, saida, valor):

    sep = ';'
    debito = str(debito).zfill(6)
    credito = str(credito).zfill(6)
    valor = converte.ajustar_casas_1_dezena_valor(valor)
    valor = valor.replace('.', '').replace(',', '').strip().zfill(14)
    descricao = descricao + ' ' + data[-7::]
    doc = '0'.zfill(14) + ' '

    lancamento = 'C' + sep + codigo_empresa + sep + \
                 doc + sep +\
                 data + sep +\
                 debito + sep + \
                 credito + sep + \
                 valor + sep + \
                 hist + sep + \
                 f'"{descricao}"' + sep

    print(lancamento, file=saida)


def DELLA_PASQUA(codigo_empresa, data, debito,
                 credito, hist, descricao, saida, valor):

    lancamento_gerencial = False

    sep = ';'
    valor = converte.ajustar_casas_1_dezena_valor(valor)
    valor = valor.replace('.', '').replace(',', '').strip().zfill(14)
    descricao = descricao + ' ' + data[-7::]
    doc = '0'.zfill(14) + ' '

    if debito[0] == '4':
        debito_gerencial = 'DDDDDD'
        credito_gerencial = '000005'
        lancamento_gerencial = True

    elif credito[0] == '4':
        debito_gerencial = 'CCCCCC'
        credito_gerencial = '000005'
        lancamento_gerencial = True

    debito = str(debito).zfill(6)
    credito = str(credito).zfill(6)

    lancamento = 'C' + sep + codigo_empresa + sep + \
                 doc + sep +\
                 data + sep +\
                 debito + sep + \
                 credito + sep + \
                 valor + sep + \
                 hist + sep + \
                 f'"{descricao}"' + sep

    print(lancamento, file=saida)

    if lancamento_gerencial:

        lancamento = 'G' + sep + codigo_empresa + sep + \
            doc + sep +\
            data + sep +\
            debito_gerencial + sep + \
            credito_gerencial + sep + \
            valor + sep + \
            hist + sep + \
            f'"{descricao}"' + sep

        print(lancamento, file=saida)
