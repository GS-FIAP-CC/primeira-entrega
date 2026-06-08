## LEITURA DOS DADOS DA MISSÃO AURORA BASE ##

#importando csv e json para que seja possivel ler os dados.
import csv
import json

""" Cada função lê um arquivo e organiza os dados na estrutura, mais adequada para o tipo de acesso necessário. """

# Função para ler o arquivo modulos_status.csv e transformar o arquivo csv em um dicionário.
def carregar_modulos(caminho):
    # abrir o arquivo e ler com DictReader
    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        # lista de dicionários
        linhas = list(leitor)   
        
     # dicionário vazio
    modulos = {}  
    # Converter os campos numéricos de tipo texto para tipo número inteiro e garantir que o status seja número inteiro.
    for linha in linhas:
         # Garantindo que o status seja número inteiro
        linha["status"] = int(linha["status"])    
        # Garantindo que a prioridade seja número inteiro
        linha["prioridade"] = int(linha["prioridade"])  
        # Usa o nome do módulo como chave do dicionário
        nome = linha["modulo"]
        modulos[nome] = linha
    return modulos

# Função para ler o arquivo energia_leituras.csv e transformar o arquivo csv em uma lista
# Usamos lista porque a ordem cronológica das leituras importa (série temporal)
def carregar_leitura_energia(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        linhas = list(leitor)

    # Convertendo as variáveis numéricas para o tipo float (valores decimais)
    for linha in linhas:
        linha["geracao_solar_kwh"] = float(linha["geracao_solar_kwh"])
        linha["geracao_eolica_kwh"] = float(linha["geracao_eolica_kwh"])
        linha["consumo_kwh"] = float(linha["consumo_kwh"])
        linha["reserva_bateria_kwh"] = float(linha["reserva_bateria_kwh"])
        linha["reserva_bateria_pct"] = float(linha["reserva_bateria_pct"])

    return linhas

# Função para ler o arquivo variaveis_ambientais.csv e transformar o arquivo csv em uma lista
# Mesma lógica da energia: é uma série temporal, então a ordem das leituras importa
def carregar_variaveis_ambientais(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        linhas = list(leitor)

    # Convertendo as variáveis numéricas para o tipo float
    for linha in linhas:
        linha["temp_externa_c"] = float(linha["temp_externa_c"])
        linha["temp_interna_c"] = float(linha["temp_interna_c"])
        linha["radiacao_msv"] = float(linha["radiacao_msv"])
        linha["vento_ms"] = float(linha["vento_ms"])
        linha["qualidade_comunicacao_pct"] = float(linha["qualidade_comunicacao_pct"])
        linha["pressao_interna_pa"] = float(linha["pressao_interna_pa"])

    return linhas


# Função para ler o arquivo log_eventos.json e retornar uma lista de eventos
# Usa o módulo json (não csv). Não precisa converter tipos, pois o JSON já preserva números e texto
def carregar_log(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados["eventos"]

# Funcao que  energia na lista de leituras, cada uma um dicionário com os dados de um momento.
def montar_matriz_energia(energia):
    #cria a lista vazia  
    matriz =[]

    # Percorre cada leitura 
    for leitura in energia:
        linha = [
            leitura["horario"],
            leitura["geracao_solar_kwh"],
            leitura["geracao_eolica_kwh"],
            leitura["consumo_kwh"],
            leitura["reserva_bateria_kwh"],
            leitura["reserva_bateria_pct"],
        ]
        # Adiciona a linha montada à matriz.
        matriz.append(linha)
    # Devolve a tabela completa    
    return matriz


def analisar_telemetria(matriz):
    ## Média de consumo no dia
    consumo = [linha[3] for linha in matriz]
    media_consumo  = sum(consumo)/len(consumo)
    
    ## Menor reserva do dia
    reserva = [linha[5] for linha in matriz]
    menor_reserva = min(reserva)

    ## Balanço energético (geração - consumo) por horário
    balanco = []
    #Percorre cada linha
    for linha in matriz:
        # Recupera o horário
        horario = linha[0]
        saldo = linha[1] + linha[2] - linha[3]
        # Guarda o resultado como tupla
        balanco.append((horario, saldo))
        
    # Devolve os três indicadores de uma vez.    
    return media_consumo, menor_reserva, balanco
