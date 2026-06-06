####################################################################
# PREVISÃO DE DADOS DA MISSÃO AURORA BASE
#   Aplica regressão linear (método dos mínimos quadrados) para
# estimar o comportamento futuro da reserva de energia. Também
# oferece a média móvel como técnica de comparação.
####################################################################


## Calcula a reta de melhor ajuste (y = a*x + b) pelo método dos mínimos quadrados
def regressao_linear(xs, ys):
    n = len(xs)              # quantidade de pontos de dados

    ## Somatórias necessárias para a fórmula dos mínimos quadrados
    soma_x  = sum(xs)                                   # soma de todos os X
    soma_y  = sum(ys)                                   # soma de todos os Y
    soma_xy = sum(xs[i] * ys[i] for i in range(n))      # soma dos produtos X*Y
    soma_x2 = sum(xi ** 2 for xi in xs)                 # soma dos X ao quadrado

    ## Coeficiente angular (inclinação): quanto Y varia a cada passo de X
    a = (n * soma_xy - soma_x * soma_y) / (n * soma_x2 - soma_x ** 2)
    ## Coeficiente linear (intercepto): valor de Y quando X = 0
    b = (soma_y - a * soma_x) / n

    return round(a, 4), round(b, 4)   # arredonda para evitar imprecisão de ponto flutuante


## Aplica a reta (y = a*x + b) para estimar o valor em um ponto X futuro
def prever_proximo_valor(a, b, x_proximo):
    y_previsto = a * x_proximo + b
    return round(y_previsto, 4)


## Prevê a reserva de energia do próximo ciclo a partir dos dados de telemetria
def prever_reserva_energetica(telemetria):
    ## Extrai apenas a série da reserva de cada leitura (list comprehension)
    reservas = [item["reserva_bateria_pct"] for item in telemetria]
    ## Cria os índices de tempo (0, 1, 2, ...) com o mesmo tamanho da série
    x = list(range(len(reservas)))

    ## Calcula a reta de tendência da reserva
    m, b = regressao_linear(x, reservas)

    ## Projeta a reserva para o próximo ciclo (o índice seguinte ao último)
    prox_ponto = prever_proximo_valor(m, b, len(reservas))

    ## Retorna: histórico completo, previsão do próximo ciclo e tendência (m)
    ## m negativo indica reserva caindo; positivo indica subindo
    return reservas, prox_ponto, m


## Calcula a média dos últimos valores da série (técnica de comparação)
def media_movel(valores, janela=3):
    ultimos_valores = valores[-janela:]              # pega os últimos N valores
    media = sum(ultimos_valores) / len(ultimos_valores)
    return media
