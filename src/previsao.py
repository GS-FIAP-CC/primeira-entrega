import config


def regressao_linear(xs, ys):
    n = len(xs)
    soma_x  = sum(xs)
    soma_y  = sum(ys)
    soma_xy = sum(xs[i] * ys[i] for i in range(n))
    soma_x2 = sum(xi ** 2 for xi in xs)

    a = (n * soma_xy - soma_x * soma_y) / (n * soma_x2 - soma_x ** 2)
    b = (soma_y - a * soma_x) / n

    return round(a, 4), round(b, 4)


def prever_proximo_valor(a, b, x_proximo):
    y_previsto = a*x_proximo + b

    return round(y_previsto, 4)


def prever_reserva_energetica(telemetria):
    pass


def media_movel(valores, janela=3):
    pass
