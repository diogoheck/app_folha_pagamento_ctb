import calendar


def calcula_data(mes, ano):
    if mes == 'JANEIRO' or mes == '01':
        return (calendar.monthrange(int(ano), 1)[1], '01')
    elif mes == 'FEVEREIRO' or mes == '02':
        return (calendar.monthrange(int(ano), 2)[1], '02')
    elif mes == 'MARCO' or mes == 'MARÇO' or mes == '03':
        return (calendar.monthrange(int(ano), 3)[1], '03')
    elif mes == 'ABRIL' or mes == '04':
        return (calendar.monthrange(int(ano), 4)[1], '04')
    elif mes == 'MAIO' or mes == '05':
        return (calendar.monthrange(int(ano), 5)[1], '05')
    elif mes == 'JUNHO' or mes == '06':
        return (calendar.monthrange(int(ano), 6)[1], '06')
    elif mes == 'JULHO' or mes == '07':
        return (calendar.monthrange(int(ano), 7)[1], '07')
    elif mes == 'AGOSTO' or mes == '08':
        return (calendar.monthrange(int(ano), 8)[1], '08')
    elif mes == 'SETEMBRO' or mes == '09':
        return (calendar.monthrange(int(ano), 9)[1], '09')
    elif mes == 'OUTUBRO' or mes == '10':
        return (calendar.monthrange(int(ano), 10)[1], '10')
    elif mes == 'NOVEMBRO' or mes == '11':
        return (calendar.monthrange(int(ano), 11)[1], '11')
    elif mes == 'DEZEMBRO' or mes == '12':
        return (calendar.monthrange(int(ano), 12)[1], '12')


def ler_data(caminho):
    with open(caminho, 'r') as arquivo:
        for registro in arquivo:
            data = registro.strip().split('/')

            nova_data = calcula_data(data[0], data[1])

            data_arquivo = str(nova_data[0]) + \
                '/' + nova_data[1] + '/' + data[1]
    return data_arquivo
