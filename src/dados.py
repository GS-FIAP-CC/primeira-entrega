## LEITURA DOS DADOS DA MISSÃO AURORA BASE ##

#importando csv e json para que seja possivel ler os dados.
import csv
import json

""" Cada função lê um arquivo e organiza os dados na estrutura, mais adequada para o tipo de acesso necessário. """

# Função para ler o arquivo modulos_status.csv e transformar o arquivo csv em um dicionário, no qual foi usado usamos porque o sistema acessa os módulos pelo nome (ex: modulos["suporte_vida"]).
def carregar_modulos(caminho):
    # Abrir o arquivo e ler com DictReader.
    with open(caminho, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
         # Lista de dicionários
        linhas = list(leitor)  

    # Dicionário vazio.
    modulos = {}             
    for linha in linhas:
        # Converter os campos numéricos de tipo texto para tipo número inteiro e garantir que o status seja número inteiro.
        linha["status"] = int(linha["status"])  
        # Garantindo que a prioridade seja número inteiro.
        linha["prioridade"] = int(linha["prioridade"])  
        # Usa o nome do módulo como chave do dicionário.
        nome = linha["modulo"]
        modulos[nome] = linha
    return modulos

# Função para ler o arquivo energia_leituras.csv e transformar o arquivo csv em uma lista e usamos lista porque a ordem cronológica das leituras importa (série temporal)
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

# Função para ler o arquivo variaveis_ambientais.csv e transformar o arquivo csv em uma lista, mesma lógica da energia: é uma série temporal, então a ordem das leituras importa
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


# Função para ler o arquivo log_eventos.json e retornar uma lista de eventos e Usa o módulo json (não csv). Não precisa converter tipos, pois o JSON já preserva números e texto
def carregar_log(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados["eventos"]
