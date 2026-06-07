import config

def gerar_recomendacoes(diagnostico, prev):
    recomendacoes = []
    historico, proximo, tendencia = prev

    # ===== 1. MÓDULO VITAL (prioridade máxima) =====
    if diagnostico["modulos"].get(config.MODULO_VITAL) == "critico":
        recomendacoes.append(("Crítica", "acionar protocolo de suporte à vida"))

    # ===== 2. ENERGIA =====
    if diagnostico["energia"] == "critico":
        recomendacoes.append(("Energia em estado crítico", "desligar módulos não essenciais e verificar sistemas de geração"))
    elif diagnostico["energia"] == "alerta":
        recomendacoes.append(("Energia em estado de alerta", "ativar modo economia de energia"))

    # ===== 3. AMBIENTE (radiação/habitat) =====
    if diagnostico["ambiente"] == "critico":
        recomendacoes.append(("Condições ambientais críticas", "verificar radiação e isolamento do habitat"))
    elif diagnostico["ambiente"] == "alerta":
        recomendacoes.append(("Condições ambientais perigosas", "realizar inspeção preventiva do habitat"))

    # ===== 4. COMUNICAÇÃO =====
    if diagnostico["comunicacao"] == "critico":
        recomendacoes.append(("Canais de comunicação comprometidos", "estabelecer canal de comunicação alternativo"))
    elif diagnostico["comunicacao"] == "alerta":
        recomendacoes.append(("Falhas nos sistemas de comunicação", "verificar antenas e transmissores"))

    # ===== 5. PREVISÃO (reserva projetada) =====
    if proximo < config.RESERVA_ALERTA_MIN:
        recomendacoes.append(("Reserva energética abaixo de 25%", "reduzir consumo de módulos não essenciais"))
    elif proximo < config.RESERVA_NORMAL_MIN and tendencia < 0:
        recomendacoes.append(("Reserva energética em alerta", "otimizar uso da reserva energética"))

    # ===== 6. TUDO NORMAL (se nada foi adicionado) =====
    if not recomendacoes:
        recomendacoes.append(("Sistemas operando normalmente", "manter monitoramento de rotina"))

    return recomendacoes



