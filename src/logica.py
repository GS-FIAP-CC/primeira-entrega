##

# Traz o modulo config para este.
import config

#Fila: FIFO - First In First Out
class Fila:
    def __init__(self):
        # lista vazia que guarda os itens
        self.itens = []

    def enfileirar(self, item):
        # Item novo entra sempre no fim da fila.
        self.itens.append(item)

    def desenfileirar(self):
        # Remove e devolve o item mais antigo, o do inicio. 
        if self.itens:
            return self.itens.pop(0)
        #Se vazia, devolve None.
        return None

    def vazia(self):
        # Verifica se a estrutura e devolve True se estiver vazia.
        return len(self.itens) == 0

    def tamanho(self):
        # Devolve quantos itens existem na estrutura.
        return len(self.itens)

#Pilha LIFO - Last in First Out
class Pilha:
    def __init__(self):
        # pilha vazia que guarda os itens
        self.itens = []

    def empilhar(self, item):
        # Item novo vai para o topo.
        self.itens.append(item)

    def desempilhar(self):
        # Remove e devolve o item do topo. 
        if self.itens:
            return self.itens.pop()
        #Se vazia, devolve None.
        return None

    def topo(self):
        # Verifica o topo sem remover e se esticer vazia retorna como NONE.
        return self.itens[-1] if self.itens else None

    def vazia(self):
        # Verifica se a estrutura e devolve True se estiver vazia.
        return len(self.itens) == 0

    def tamanho(self):
        # Devolve quantos itens existem na estrutura.
        return len(self.itens)

#Funcao de avaliacao - Classifica um módulo como normal, alerta, crítico ou desconhecido.
def classificar_modulo(nome, telemetria):
    modulos = telemetria["modulos"]
    # Se o modulo nao existe na telemetria, retorna como desconhecido.
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

def detectar_anomalias(telemetria):
    anomalias = []

    energia = telemetria["energia"]
    ambiente = telemetria["ambiente"]
    modulos = telemetria["modulos"]

    for i in range(len(energia)):
        leitura_energia = energia[i]
        leitura_ambiente = ambiente[i]
        geracao_solar = leitura_energia["geracao_solar_kwh"]
        radiacao = leitura_ambiente["radiacao_msv"]

        ## Anomalia 1: geração de energia solar a noite
        if radiacao == 0 and geracao_solar > 0:
            anomalias.append(f"Anomalia detectada às {leitura_energia['horario']}: geração solar de {geracao_solar} kWh durante a noite (radiação zero)")

        ## Anomalia 2: valores fora da realidade (< 0% e > 100%)
        reserva = leitura_energia["reserva_bateria_pct"]
        if reserva > 100 or reserva < 0:
            anomalias.append(f"Anomalia detectada às {leitura_energia['horario']}: armazenamento fora da realidade ({reserva})")
        
        ## Anomalia 3: módulos desligados e gerando energia
        status_eolica = modulos["energia_eolica"]["status"]
        geracao_eolica = leitura_energia["geracao_eolica_kwh"]
        if status_eolica == 0 and geracao_eolica > 0:
            anomalias.append(f"Anomalia detectada às {leitura_energia['horario']}: geração de energia eólica com as turbinas desligadas")

        status_solar = modulos["energia_solar"]["status"]
        geracao_solar = leitura_energia["geracao_solar_kwh"]
        if status_solar == 0 and geracao_solar > 0:
            anomalias.append (f"Anomalia detectada às {leitura_energia['horario']}: geração de energia solar com os paineis desligados")

    return anomalias
