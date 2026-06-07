## LOGICA ##

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

    #Esta puxando os dados de um módulo específico de dentro da telemetria.
    info = modulos[nome]
    #Sendo que 1 significa ligado e 0 desligado
    status = info["status"]
    criticidade = info["criticidade"]

    # Se o status estiver desligado, sera igual ao critico
    if status == 0 and criticidade == "critico":
        return "critico"
    # Caso contrário, basta estar desligado ou marcado como alerta.
    elif status == 0 or criticidade == "alerta":
        return "alerta"  
    #Caso contrario sera como normal.
    else:
        return "normal"

#Avalia o subsistema de energia com base na leitura mais recente. 
def avaliar_energia(telemetria):
    # [-1] pega a leitura mais recente
    leitura = telemetria["energia"][-1]
    reserva = leitura["reserva_bateria_pct"]
    geracao = leitura["geracao_solar_kwh"] + leitura["geracao_eolica_kwh"]
    consumo = leitura["consumo_kwh"]

    # No estado critico exige duas coisas juntos, a reserva baixa e deficit de energia. 
    if reserva < config.RESERVA_ALERTA_MIN and consumo > geracao:
        return "critico"
    # Alerta é leve, onde reserva abaixo do normal, ou perdendo energia com reserva ainda moderada.
    elif reserva < config.RESERVA_NORMAL_MIN or (consumo > geracao and reserva < config.RESERVA_MODERADA_MAX):
        return "alerta"
    # Caso contrario retorna como normal
    else:
        return "normal"

# Avalia a qualidade da comunicação na leitura ambiental mais recente.
def avaliar_comunicacao(telemetria):
    qualidade = telemetria["ambiente"][-1]["qualidade_comunicacao_pct"]
    # No estado critico exige que a qualidade seja menor do que a comunicacao alerta por minuto
    if qualidade < config.COMUNICACAO_ALERTA_MIN:
        return "critico"
    # Se nao, a qualidade foi maior ou igual a comunicacao normal sera um Alerta
    elif not (qualidade >= config.COMUNICACAO_NORMAL_MIN):
        return "alerta"
    #Caso contrario Normal.
    else:
        return "normal"

#Avalia radiação e temperatura interna do habitat na leitura mais recente.
def avaliar_radiacao_habitat(telemetria):
    # [-1] pega a leitura mais recente
    leitura = telemetria["ambiente"][-1]
    radiacao = leitura["radiacao_msv"]
    temp = leitura["temp_interna_c"]

    # Comparacao da temperatura dentro da faixa segura
    temp_ok = config.TEMP_INTERNA_MIN <= temp <= config.TEMP_INTERNA_MAX
    
    # Crítico só quando os problemas da radiação alta e a temperatura estiverem fora da faixa.
    if radiacao >= config.RADIACAO_CRITICO_MIN and not temp_ok:
        return "critico"
    # Alerta quando qualquer um dos dois estiverem fora da faixa.
    elif radiacao >= config.RADIACAO_ALERTA_MIN or not temp_ok:
        return "alerta"
    #Caso contrario retorna como normal.
    else:
        return "normal"

#Funcao que decide se a base entra em estado crítico.
def expressao_booleana_principal(telemetria):
    energia = avaliar_energia(telemetria)
    comunicacao = avaliar_comunicacao(telemetria)
    ambiente = avaliar_radiacao_habitat(telemetria)
    suporte = classificar_modulo(config.MODULO_VITAL, telemetria)

    # Retorna True quando qualquer subsistema vital está crítico.
    return (
        energia == "critico"
        or ambiente == "critico"
        or suporte == "critico"
        or (energia == "alerta" and comunicacao == "critico")
    )

#Monta um diagnostico geral, juntando todos os subsistemas.
def diagnosticar(telemetria, eventos=None):
    #Avalia energia, comunicação, ambiente e de cada módulo.
    diag_energia = avaliar_energia(telemetria)
    diag_comunicacao = avaliar_comunicacao(telemetria)
    diag_ambiente = avaliar_radiacao_habitat(telemetria)

    # Classifica cada módulo presente na telemetria.
    diag_modulos = {}
    for nome in telemetria["modulos"]:
        diag_modulos[nome] = classificar_modulo(nome, telemetria)
        
    #Organiza os alertas em fila e os criticos em pilha.
    fila_alertas = Fila()
    pilha_criticos = Pilha()

    # Pega os eventos antigos e os críticos vão para a pilha com prefixo "historico:" para distingui-los dos atuais.
    if eventos:
        for ev in eventos:
            # .get evita erro se a chave não existir
            if ev.get("severidade") == "critico":
                pilha_criticos.empilhar("historico:" + ev["modulo_afetado"])

    # Processa os três subsistemas.
    subsistemas = [
        ("energia", diag_energia),
        ("comunicacao", diag_comunicacao),
        ("ambiente", diag_ambiente),
    ]
    
    # Percorre os subsistemas
    for nome, situacao in subsistemas:
        # Se a situacao está em alerta entra na fila.
        if situacao == "alerta":
            fila_alertas.enfileirar(nome)
        # Se está crítico entra na fila e também na pilha de críticos.
        elif situacao == "critico":
            fila_alertas.enfileirar(nome)
            pilha_criticos.empilhar(nome)
            
    # Percorre os modulos
    for nome, situacao in diag_modulos.items():
        # Prefixo "modulo:" para diferenciar um módulo de um subsistema na lista de alertas.
        rotulo = "modulo:" + nome
        # Se a situacao está em alerta entra na fila.
        if situacao == "alerta":
            fila_alertas.enfileirar(rotulo)
        # Se está crítico entra na fila e também na pilha de críticos.
        elif situacao == "critico":
            fila_alertas.enfileirar(rotulo)
            pilha_criticos.empilhar(rotulo)
            
    #Se a situação for crítica o estado é "critico".
    if expressao_booleana_principal(telemetria):
        estado = "critico"
    #se houver qualquer alerta pendente na fila, o estado é "alerta"
    elif not fila_alertas.vazia():
        estado = "alerta"
    #Caso contrario retorna como normal.
    else:
        estado = "normal"

    #Monta um dicionario
    return {
        "estado": estado,
        "energia": diag_energia,
        "comunicacao": diag_comunicacao,
        "ambiente": diag_ambiente,
        "modulos": diag_modulos,
        # Cópia da lista para não expor a interna.
        "alertas_pendentes": list(fila_alertas.itens),
        #Topo para o critico ser o mais recente.
        "ultimo_evento_critico": pilha_criticos.topo(),
    }

#Procura inconsistencia nos dados
def detectar_anomalias(telemetria):
    
    anomalias = []

    energia = telemetria["energia"]
    ambiente = telemetria["ambiente"]
    modulos = telemetria["modulos"]

    # Percorre todas as leituras pelo índice.
    for i in range(len(energia)):
        leitura_energia = energia[i]
        leitura_ambiente = ambiente[i]
        geracao_solar = leitura_energia["geracao_solar_kwh"]
        radiacao = leitura_ambiente["radiacao_msv"]

        ## Anomalia 1: geração de energia solar a noite
        if radiacao == 0 and geracao_solar > 0:
            #Se não há radiação (noite) mas há geração solar, algo está errado fisicamente.
            anomalias.append(f"Anomalia detectada às {leitura_energia['horario']}: geração solar de {geracao_solar} kWh durante a noite (radiação zero)")

        ## Anomalia 2: valores fora da realidade (< 0% e > 100%)
        reserva = leitura_energia["reserva_bateria_pct"]
        if reserva > 100 or reserva < 0:
            #Porcentagem de bateria fora de 0–100% é impossível, ou seja provável erro de sensor.
            anomalias.append(f"Anomalia detectada às {leitura_energia['horario']}: armazenamento fora da realidade ({reserva})")
        
        ## Anomalia 3: módulos desligados e gerando energia
        status_eolica = modulos["energia_eolica"]["status"]
        geracao_eolica = leitura_energia["geracao_eolica_kwh"]
        #Se um módulo está desligado (status == 0) mas ainda reporta geração, é inconsistência. 
        if status_eolica == 0 and geracao_eolica > 0:
            anomalias.append(f"Anomalia detectada às {leitura_energia['horario']}: geração de energia eólica com as turbinas desligadas")

        status_solar = modulos["energia_solar"]["status"]
        geracao_solar = leitura_energia["geracao_solar_kwh"]
        if status_solar == 0 and geracao_solar > 0:
            anomalias.append (f"Anomalia detectada às {leitura_energia['horario']}: geração de energia solar com os paineis desligados")

    #Retorna a lista de todas as anomalias encontradas.
    return anomalias
