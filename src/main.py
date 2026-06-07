#Importando os e sys para ler argumentos da linha de comando.
import os
import sys
#Importando os modulos de leitura de dados, diagnóstico, previsão e recomendações.
import dados
import logica
import previsao
import recomendacoes

#__file__ é o caminho deste ficheiro, o 'dirname' sobe para a pasta onde está o main.py, ja o segundo dirname sobe mais um nível.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#sys.argv[0] é o nome do script, e ira pegar os argumentos passados.
def parsear_argumentos():
    args = sys.argv[1:]
    pasta = os.path.join(PROJECT_ROOT, "data")    
    #Percorre a lista, devolvendo a cada volta um par. 
    for i, a in enumerate(args):
        # Procura -d/--dados seguido de um caminho, enquando o i + 1 <len(args) garante que existe um valor.
        if a in ("-d", "--dados") and i + 1 < len(args):
            pasta = args[i + 1]
    return pasta

#Ajustando o cabeçalho para que fique mais facil a leitura
def imprimir_cabecalho(titulo):
    print()
    print("=" * 60)
    print(titulo.center(60))
    print("=" * 60)

#Ajustando o dignostico para facilitar a leitura
def imprimir_diagnostico(d):
    imprimir_cabecalho("DIAGNÓSTICO DA MISSÃO")
    print(f"Estado global: {d['estado'].upper()}\n")
    print(f"  Energia ..... {d['energia']}")
    print(f"  Comunicação . {d['comunicacao']}")
    print(f"  Ambiente .... {d['ambiente']}\n")
    
    # {nome:<15} alinha o nome à esquerda num campo de 15, para os status ficarem em colunas.
    print("Módulos:")
    for nome, status in d["modulos"].items():
        print(f"  - {nome:<15} {status}")
    #Se a lista de alertas não estiver vazia, imprime cada um, o FIFO indica que a ordem da lista é a de chegada.
    print("\nAlertas pendentes (FIFO):")
    if d["alertas_pendentes"]:
        for a in d["alertas_pendentes"]:
            print(f"  -> {a}")
    #Se a lista estiver fazer, sera impresso "nenhum"
    else:
        print("  (nenhum)")
    
    # Condicional acima cobre tanto None como string vazia.
    ultimo = d["ultimo_evento_critico"]
    print(f"\nÚltimo evento crítico: {ultimo if ultimo else '(nenhum)'}")

#Define que a tupla é de três elementos, desempacotada de uma vez.
def imprimir_previsao(prev):
    historico, proximo, tendencia = prev
    ### 
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
