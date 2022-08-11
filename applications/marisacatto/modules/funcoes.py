class Funcoes():
    def __init__()
        ṕass
        
    def data_regressiva(data):
        ano= 2019       #formato AAA
        mes=  5       #usar numeros
        dia= data
        import datetime

        datapadrao = datetime.date(ano, mes, dia)
        hoje = datetime.date.today()

        if datapadrao > hoje:
            delta = datapadrao - hoje

        elif datapadrao <= hoje:
            delta = hoje - datapadrao

        resultado_delta = delta.days
        return resultado_delta

teste = Funcoes.data_regressiva(5)

print(teste)