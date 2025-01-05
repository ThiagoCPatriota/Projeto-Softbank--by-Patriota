import requests
def validador_cpf(cpf):
    cpf_c = ''
    aux = 10
    result = 0
    for i in range(9):
        cpf_c += cpf[i]
    for i in range(9):
        result += int(cpf_c[i]) * aux
        aux -= 1
    result = (result*10)%11
    result = result if result < 10 else 0
    cpf_c += str(result)

    result = 0
    aux = 11
    for i in range(10):
        result += int(cpf_c[i]) * aux
        aux -= 1
    result = (result*10)%11
    result = result if result < 10 else 0
    cpf_c += str(result)
    if cpf_c == cpf:
        return True
    return False

#CPF VALIDO PARA TESTES:    64042544096

def obter_cotacao_bitcoin():
    url = "https://economia.awesomeapi.com.br/last/BTC-BRL"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        cotacao_dolar = dados['BTCBRL']['bid']

        return cotacao_dolar
    else:

        return "Erro ao obter a cotação"
    
