import os
import sys
import dados
import logica
import previsao
import recomendacoes


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parsear_argumentos():
    args = sys.argv[1:]
    pasta = os.path.join(PROJECT_ROOT, "data")
    for i, a in enumerate(args):
        if a in ("-d", "--dados") and i + 1 < len(args):
            pasta = args[i + 1]
    return pasta


def imprimir_cabecalho(titulo):
    print()
    print("=" * 60)
    print(titulo.center(60))
    print("=" * 60)


def imprimir_diagnostico(d):
    imprimir_cabecalho("DIAGNÓSTICO DA MISSÃO")
    print(f"Estado global: {d['estado'].upper()}\n")
    print(f"  Energia ..... {d['energia']}")
    print(f"  Comunicação . {d['comunicacao']}")
    print(f"  Ambiente .... {d['ambiente']}\n")

    print("Módulos:")
    for nome, status in d["modulos"].items():
        print(f"  - {nome:<15} {status}")

    print("\nAlertas pendentes (FIFO):")
    if d["alertas_pendentes"]:
        for a in d["alertas_pendentes"]:
            print(f"  -> {a}")
    else:
        print("  (nenhum)")

    ultimo = d["ultimo_evento_critico"]
    print(f"\nÚltimo evento crítico: {ultimo if ultimo else '(nenhum)'}")


def imprimir_previsao(prev):
    historico, proximo, tendencia = prev
    imprimir_cabecalho("PREVISÃO DE RESERVA ENERGÉTICA")
    print("Histórico (% de bateria):")
    for i, v in enumerate(historico):
        print(f"  ciclo {i}: {v:.1f}%")
    print(f"\nPróximo ciclo previsto: {proximo:.1f}%")
    if tendencia > 0:
        sentido = "subindo"
    elif tendencia < 0:
        sentido = "caindo"
    else:
        sentido = "estável"
    print(f"Tendência: {tendencia:+.4f} pp/ciclo ({sentido})")


def imprimir_recomendacoes(recs):
    imprimir_cabecalho("RECOMENDAÇÕES")
    if not recs:
        print("Nenhuma recomendação no momento.")
        return
    for i, r in enumerate(recs, 1):
        print(f"{i}. {r}")


def main():
    pasta = parsear_argumentos()

    modulos = dados.carregar_modulos(f"{pasta}/modulos_status.csv")
    energia = dados.carregar_leitura_energia(f"{pasta}/energia_leituras.csv")
    ambiente = dados.carregar_variaveis_ambientais(f"{pasta}/variaveis_ambientais.csv")
    eventos = dados.carregar_log(f"{pasta}/log_eventos.json")

    telemetria = {"modulos": modulos, "energia": energia, "ambiente": ambiente}

    diagnostico = logica.diagnosticar(telemetria, eventos)
    imprimir_diagnostico(diagnostico)

    prev = previsao.prever_reserva_energetica(energia)
    imprimir_previsao(prev)

    gerar = getattr(recomendacoes, "gerar_recomendacoes", None)
    recs = gerar(diagnostico, prev) if gerar else []
    imprimir_recomendacoes(recs)


if __name__ == "__main__":
    main()
