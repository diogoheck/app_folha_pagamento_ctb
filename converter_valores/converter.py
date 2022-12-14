def isnumber(valor):
    try:
        float(valor)
    except ValueError:
        return False
    return True


def auxiliar_ajustar_casas(valor, div):
    valor_acresc = ''
    novo_valor = ''

    valor = valor.split(div)
    if(len(valor[1])) == 1:

        valor_acresc = valor[1] + '0'

        novo_valor = valor[0] + valor_acresc

        return novo_valor
    else:
        return valor[0] + valor[1]


def ajustar_casas_1_dezena_valor(valor):
    valor = str(valor)

    if '.' in valor:
        valor = auxiliar_ajustar_casas(valor, '.')

    elif ',' in valor:
        valor = auxiliar_ajustar_casas(valor, ',')

    else:
        valor = valor + '00'

    return valor


def converte_valor_string_separacao_ponto(valor):

    valor = str(valor)

    if '.' in valor and ',' in valor:

        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')

    elif ',' in valor:

        valor = valor.replace(',', '.')

    return valor


def converte_valor_string(valor):

    valor = str(valor)

    if '.' in valor and ',' in valor:
        valor = valor.replace('.', '')
    else:
        valor = valor.replace('.', ',')
    return valor


def converte_valor_float(*texto):
    soma = 0.0

    for te in texto:
        if isnumber(te):
            valor = te
        elif '.' in te and ',' in te:
            valor = te.replace('.', '').replace(',', '.')
        else:
            valor = te.replace(',', '.')

        soma = float(valor) + soma
    soma = round(soma, 2)
    return soma


if __name__ == '__main__':
    print(isnumber('14.56'))
