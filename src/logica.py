import config


class Fila:
    def __init__(self):
        self.itens = []

    def enfileirar(self, item):
        self.itens.append(item)

    def desenfileirar(self):
        if self.itens:
            return self.itens.pop(0)
        return None

    def vazia(self):
        return len(self.itens) == 0

    def tamanho(self):
        return len(self.itens)


class Pilha:
    def __init__(self):
        self.itens = []

    def empilhar(self, item):
        self.itens.append(item)

    def desempilhar(self):
        if self.itens:
            return self.itens.pop()
        return None

    def topo(self):
        return self.itens[-1] if self.itens else None

    def vazia(self):
        return len(self.itens) == 0

    def tamanho(self):
        return len(self.itens)


def classificar_modulo(nome, telemetria):
    modulos = telemetria["modulos"]
    if nome not in modulos:
        return "desconhecido"

    info = modulos[nome]
    status = info["status"]
    criticidade = info["criticidade"]

    if status == 0 and criticidade == "critico":
        return "critico"
    elif status == 0 or criticidade == "alerta":
        return "alerta"
    else:
        return "normal"


def avaliar_energia(telemetria):
    leitura = telemetria["energia"][-1]
    reserva = leitura["reserva_bateria_pct"]
    geracao = leitura["geracao_solar_kwh"] + leitura["geracao_eolica_kwh"]
    consumo = leitura["consumo_kwh"]

    if reserva < config.RESERVA_ALERTA_MIN and consumo > geracao:
        return "critico"
    elif reserva < config.RESERVA_NORMAL_MIN or (consumo > geracao and reserva < config.RESERVA_MODERADA_MAX):
        return "alerta"
    else:
        return "normal"


def avaliar_comunicacao(telemetria):
    qualidade = telemetria["ambiente"][-1]["qualidade_comunicacao_pct"]

    if qualidade < config.COMUNICACAO_ALERTA_MIN:
        return "critico"
    elif not (qualidade >= config.COMUNICACAO_NORMAL_MIN):
        return "alerta"
    else:
        return "normal"


def avaliar_radiacao_habitat(telemetria):
    leitura = telemetria["ambiente"][-1]
    radiacao = leitura["radiacao_msv"]
    temp = leitura["temp_interna_c"]

    temp_ok = config.TEMP_INTERNA_MIN <= temp <= config.TEMP_INTERNA_MAX

    if radiacao >= config.RADIACAO_CRITICO_MIN and not temp_ok:
        return "critico"
    elif radiacao >= config.RADIACAO_ALERTA_MIN or not temp_ok:
        return "alerta"
    else:
        return "normal"


def expressao_booleana_principal(telemetria):
    energia = avaliar_energia(telemetria)
    comunicacao = avaliar_comunicacao(telemetria)
    ambiente = avaliar_radiacao_habitat(telemetria)
    suporte = classificar_modulo(config.MODULO_VITAL, telemetria)

    return (
        energia == "critico"
        or ambiente == "critico"
        or suporte == "critico"
        or (energia == "alerta" and comunicacao == "critico")
    )


def diagnosticar(telemetria, eventos=None):
    diag_energia = avaliar_energia(telemetria)
    diag_comunicacao = avaliar_comunicacao(telemetria)
    diag_ambiente = avaliar_radiacao_habitat(telemetria)

    diag_modulos = {}
    for nome in telemetria["modulos"]:
        diag_modulos[nome] = classificar_modulo(nome, telemetria)

    fila_alertas = Fila()
    pilha_criticos = Pilha()

    if eventos:
        for ev in eventos:
            if ev.get("severidade") == "critico":
                pilha_criticos.empilhar("historico:" + ev["modulo_afetado"])

    subsistemas = [
        ("energia", diag_energia),
        ("comunicacao", diag_comunicacao),
        ("ambiente", diag_ambiente),
    ]
    for nome, situacao in subsistemas:
        if situacao == "alerta":
            fila_alertas.enfileirar(nome)
        elif situacao == "critico":
            fila_alertas.enfileirar(nome)
            pilha_criticos.empilhar(nome)

    for nome, situacao in diag_modulos.items():
        rotulo = "modulo:" + nome
        if situacao == "alerta":
            fila_alertas.enfileirar(rotulo)
        elif situacao == "critico":
            fila_alertas.enfileirar(rotulo)
            pilha_criticos.empilhar(rotulo)

    if expressao_booleana_principal(telemetria):
        estado = "critico"
    elif not fila_alertas.vazia():
        estado = "alerta"
    else:
        estado = "normal"

    return {
        "estado": estado,
        "energia": diag_energia,
        "comunicacao": diag_comunicacao,
        "ambiente": diag_ambiente,
        "modulos": diag_modulos,
        "alertas_pendentes": list(fila_alertas.itens),
        "ultimo_evento_critico": pilha_criticos.topo(),
    }
