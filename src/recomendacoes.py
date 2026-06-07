## RECOMENDACOES DO PROJETO ##
#Traz o modo config para este
import config

# Recebe o diagnóstico já processado e a previsão de energia, devolvendo a lista de recomendações priorizadas
def gerar_recomendacoes(diagnostico, prev):
    recomendacoes = []
    # Deixando a preivao em tupla
    historico, proximo, tendencia = prev

    # É o modo de suporte à vida, sendo prioridade maximo.
    if diagnostico["modulos"].get(config.MODULO_VITAL) == "critico":
        recomendacoes.append(("Crítica", "acionar protocolo de suporte à vida"))

    # Campo energia, onde guarda um rótulo de estado, comparando o com critico.
    if diagnostico["energia"] == "critico":
        recomendacoes.append(("Energia em estado crítico", "desligar módulos não essenciais e verificar sistemas de geração"))
    # Se nao for critico, sera o "alerta".
    elif diagnostico["energia"] == "alerta":
        recomendacoes.append(("Energia em estado de alerta", "ativar modo economia de energia"))

    # Campo de Ambiente, se nao for critico, recebera o alerta.
    if diagnostico["ambiente"] == "critico":
        recomendacoes.append(("Condições ambientais críticas", "verificar radiação e isolamento do habitat"))
    elif diagnostico["ambiente"] == "alerta":
        recomendacoes.append(("Condições ambientais perigosas", "realizar inspeção preventiva do habitat"))

    # Campo de comunicacao, é a mesma logica dos dois acima.
    if diagnostico["comunicacao"] == "critico":
        recomendacoes.append(("Canais de comunicação comprometidos", "estabelecer canal de comunicação alternativo"))
    elif diagnostico["comunicacao"] == "alerta":
        recomendacoes.append(("Falhas nos sistemas de comunicação", "verificar antenas e transmissores"))

    # Este modo compara o valor projetado com o limiar.
    if proximo < config.RESERVA_ALERTA_MIN:
        recomendacoes.append(("Reserva energética abaixo de 25%", "reduzir consumo de módulos não essenciais"))
    # E é exigido duas condições, sendo o valor abaixo do mínimo normal E tendencia negativa (queda projetada).
    elif proximo < config.RESERVA_NORMAL_MIN and tendencia < 0:
        recomendacoes.append(("Reserva energética em alerta", "otimizar uso da reserva energética"))

    # Se nao tiver nenhuma das condição acima disparou, sera enviado a mensagem padrao.
    if not recomendacoes:
        recomendacoes.append(("Sistemas operando normalmente", "manter monitoramento de rotina"))

    return recomendacoes



