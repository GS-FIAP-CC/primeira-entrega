
## Resumo do problema

Missões espaciais modernas operam com comunicação limitada e dependem de sistemas autônomos para interpretar telemetria, identificar situações críticas e recomendar ações. 
Este projeto simula esse sistema, recebendo dados de uma missão experimental e produzindo diagnóstico, alertas priorizados, previsão de variável crítica e recomendações.

## Equipe
 
- Eduardo Lopes da Silveira Mota -RM 563418

- Gabriel Luís de Lima Ramos - RM 568984

- Mayara Luisa Vicente Rosa - RM 571955
  
- Victor Camargo - RM 568912


## Estruturas de dados utilizadas
 - **Lista**: foi usada para armazenar séries temporais de geração solar, consumo e temperatura ao longo dos 8 horários do sol marciano. A ordem dos elementos representa a sequência cronológica das leituras.
 - **Dicionário**: usado para acessar o status e a criticidade de cada módulo diretamente pelo nome, sem precisar percorrer uma lista.
 - **Fila**: usada para organizar alertas pendentes por ordem de chegada, garantindo que o alerta mais antigo seja tratado primeiro (FIFO).
 - **Pilha**: usada para registrar os eventos críticos analisados, permitindo consultar o evento mais recente com facilidade (LIFO).
 - **Matriz**: usada para representar as leituras de telemetria por horário e variável, onde cada linha é um horário e cada coluna é uma grandeza medida.


## Regras lógicas principais

O diagnóstico final da missão sai da combinação de quatro avaliações: energia, comunicação, ambiente e a classificação de cada módulo. Cada uma devolve um rótulo (normal, alerta ou critico) e esses rótulos entram numa expressão booleana que define o estado global.

Para a energia (função `avaliar_energia` em `src/logica.py`), a regra olha para a reserva da bateria e para o balanço entre geração e consumo. Quando a reserva está abaixo de 25% e ainda por cima o consumo é maior que a geração, o sistema declara energia crítica. Se a reserva está abaixo de 50%, ou se o consumo passa a geração com a reserva ainda abaixo de 60%, o estado vira alerta. Caso contrário, energia normal.

A comunicação é avaliada pela qualidade do sinal. Abaixo de 30% é crítico. A faixa intermediária usa um NOT explícito: se NOT (qualidade >= 70%), entra em alerta. Acima de 70% é normal.

O ambiente combina radiação e temperatura interna. Se a radiação chega a 0,6 mSv e a temperatura está fora da faixa segura de 18 a 26 graus, é crítico. Se só uma das duas condições aparece (radiação a partir de 0,3 mSv ou temperatura fora de faixa), o estado é alerta.

Cada módulo individual também é classificado pela função `classificar_modulo`, que combina o status binário do módulo (0 ou 1) com a criticidade declarada no CSV. Um módulo de criticidade "critico" com status zero vira critico. Um módulo desligado de criticidade menor, ou um módulo cuja criticidade já é "alerta", vira alerta.

A expressão booleana principal do diagnóstico, presente na função `expressao_booleana_principal`, é:

```
estado_critico = energia == "critico"
              OR ambiente == "critico"
              OR suporte_vida == "critico"
              OR (energia == "alerta" AND comunicacao == "critico")
```

A lógica aqui é proteger a vida em primeiro lugar. Qualquer falha grave em energia, ambiente ou no módulo de suporte à vida coloca a missão em estado crítico. Existe ainda uma combinação de risco indireto: quando a energia já está em alerta e a comunicação cai, a base fica isolada num momento em que mais precisaria pedir apoio. Nessa situação o sistema também eleva para crítico, mesmo que cada variável isolada não esteja em valor extremo.

Quando nenhuma dessas condições é satisfeita mas existem itens na fila de alertas, o estado fica em alerta. Se a fila está vazia, o estado é normal.

Por fim, a função `detectar_anomalias` cruza dados de fontes diferentes para encontrar leituras fisicamente impossíveis, como geração solar em horário noturno, geração com módulo desligado e reservas fora do intervalo de 0 a 100%. Foi essa rotina que pegou a inconsistência proposital do dataset (geração solar de 18,5 kWh às 21h).

## Técnica de previsão

A variável crítica escolhida foi a reserva da bateria em porcentagem ao longo dos oito horários do sol marciano. A técnica aplicada é regressão linear pelo método dos mínimos quadrados, implementada do zero em `src/previsao.py`, sem nenhuma biblioteca externa.

O cálculo segue o passo a passo clássico. Primeiro o sistema monta a série de reservas, que no dataset atual é [56,0; 52,9; 50,4; 49,5; 50,9; 49,3; 45,8; 45,6], e o vetor de tempo com índices de 0 a 7. Depois calcula as somatórias de x, y, xy e x ao quadrado. Com elas, encontra o coeficiente angular pela fórmula a = (n·Σxy − Σx·Σy) / (n·Σx² − (Σx)²) e o intercepto b = (Σy − a·Σx) / n. A previsão do próximo ciclo é simplesmente ŷ = a·8 + b.

Com os dados atuais, o coeficiente angular é −1,3119 pontos percentuais por ciclo, e a reserva projetada para o próximo ciclo é de 44,1%. Como esse valor cruza o limiar de alerta de 50% e a tendência é negativa, o módulo de recomendações dispara a ação "otimizar uso da reserva energética". Esse caminho atende ao requisito do enunciado de que a previsão precisa influenciar pelo menos uma decisão do sistema.

Como técnica de comparação, o mesmo arquivo oferece a função `media_movel`, que faz uma estimativa rápida de curto prazo a partir da média dos últimos valores da série.

## Como executar

O projeto roda em Python 3.8 ou superior e usa apenas a biblioteca padrão, sem dependências externas. Da raiz do repositório:

```bash
python src/main.py
```

Por padrão o sistema lê os quatro arquivos da pasta `data/`. Caso queira apontar outra pasta de telemetria, basta usar a flag `-d` ou `--dados`:

```bash
python src/main.py -d /caminho/para/outra/pasta
```

A pasta indicada precisa conter os arquivos `modulos_status.csv`, `energia_leituras.csv`, `variaveis_ambientais.csv` e `log_eventos.json`.

## Exemplo de entrada e saída

A entrada é o pacote de telemetria da pasta `data/`. O `modulos_status.csv` lista os oito módulos da base, com a turbina eólica offline (status 0) por manutenção preventiva e o canal de comunicação rodando em criticidade alerta. O `energia_leituras.csv` mostra a reserva caindo de 56% no começo do sol marciano para 45,6% no final, e inclui a leitura suspeita de 18,5 kWh de geração solar às 21h, plantada de propósito. O `variaveis_ambientais.csv` traz a qualidade de comunicação entre 52% e 71%, radiação chegando a 0,71 mSv ao meio-dia e temperatura interna estável em torno de 21 a 22 graus. O `log_eventos.json` reúne dez eventos em sequência narrativa do Sol 147, começando pela queda da turbina, passando pela tempestade de poeira que reduz a geração solar e pela degradação da comunicação, até o diagnóstico noturno.

A saída produzida pelo sistema com essa entrada é:

```
============================================================
                   DIAGNÓSTICO DA MISSÃO
============================================================
Estado global: ALERTA

  Energia ..... alerta
  Comunicação . normal
  Ambiente .... normal

Módulos:
  - suporte_vida    normal
  - energia_solar   normal
  - energia_eolica  alerta
  - comunicacao     alerta
  - habitat         normal
  - laboratorio     normal
  - armazenamento   normal
  - baterias        normal

Alertas pendentes (FIFO):
  -> energia
  -> modulo:energia_eolica
  -> modulo:comunicacao

Último evento crítico: historico:comunicacao

============================================================
               PREVISÃO DE RESERVA ENERGÉTICA
============================================================
Histórico (% de bateria):
  ciclo 0: 56.0%
  ciclo 1: 52.9%
  ciclo 2: 50.4%
  ciclo 3: 49.5%
  ciclo 4: 50.9%
  ciclo 5: 49.3%
  ciclo 6: 45.8%
  ciclo 7: 45.6%

Próximo ciclo previsto: 44.1%
Tendência: -1.3119 pp/ciclo (caindo)

============================================================
                       RECOMENDAÇÕES
============================================================
1. Energia em estado de alerta, ativar modo economia de energia
2. Reserva energética em alerta, otimizar uso da reserva energética

============================================================
                    ANOMALIAS DETECTADAS
============================================================
1. Anomalia detectada às 21:00: geração solar de 18.5 kWh durante a noite (radiação zero)

>> Verificar funcionamento dos sensores
```

## Recomendações geradas pelo sistema

As recomendações nascem da função `gerar_recomendacoes` no arquivo `recomendacoes.py`, que cruza o diagnóstico já calculado com a previsão de energia.

A ação de mais alta prioridade é a do suporte à vida: se o módulo aparece em estado crítico, o sistema recomenda acionar o protocolo correspondente antes de qualquer outra coisa. A partir daí entram as recomendações ligadas a cada subsistema. Energia crítica pede desligar módulos não essenciais e checar geração; energia em alerta pede ativar o modo economia. Para o ambiente, condições críticas pedem verificar radiação e isolamento do habitat, enquanto o nível de alerta pede inspeção preventiva. Na comunicação, o estado crítico pede um canal alternativo, e o alerta pede checar antenas e transmissores.

As últimas duas regras vêm da previsão. Quando a projeção da reserva fica abaixo de 25%, o sistema pede redução do consumo dos módulos não essenciais. Quando fica abaixo de 50% e a tendência é negativa, recomenda otimizar o uso da reserva energética. Se nenhuma dessas condições é satisfeita, o retorno padrão é "sistemas operando normalmente, manter monitoramento de rotina".

Com o dataset de exemplo, o sistema gera duas recomendações: ativar modo economia, por causa da energia em alerta, e otimizar uso da reserva, por causa da previsão de 44,1% no próximo ciclo com tendência negativa.

## Link do vídeo

A inserir antes da entrega. O link também precisa ser copiado para o arquivo `docs/link_video.txt`.

## Conclusões e aprendizados

A separação do código em módulos (dados, lógica, previsão e recomendações) foi a decisão que mais facilitou o trabalho. Cada parte ficou possível de testar isoladamente e mexer em um limiar virou questão de editar uma constante, não de procurar a regra escondida no meio de outra função.

A escolha das estruturas de dados também passou a fazer mais sentido depois que cada uma resolveu um problema concreto. O dicionário deu acesso direto ao status de um módulo pelo nome, sem precisar varrer lista. A lista preservou a ordem cronológica das leituras, que importa para a previsão. A fila modelou o tratamento de alertas pendentes na ordem de chegada e a pilha permitiu consultar rapidamente o último evento crítico analisado.

Reduzir o estado global da missão a uma única expressão booleana ajudou a tornar o diagnóstico auditável. Quem lê o código consegue entender em poucas linhas o que faz a missão entrar em estado crítico, e isso é bem diferente de espalhar a decisão em vários ifs aninhados.

A inconsistência da geração solar à noite só apareceu porque o sistema cruzou dois arquivos diferentes. Foi um lembrete prático de que sensores podem falhar e que o software precisa desconfiar do dado, não só processá-lo. Em uma operação real, ignorar essa leitura suspeita poderia gerar uma previsão otimista demais e levar a decisões erradas sobre consumo.

A previsão por regressão linear, mesmo simples e feita à mão, foi suficiente para antecipar a queda da reserva e disparar uma recomendação preventiva. Não foi necessário recorrer a bibliotecas de machine learning para extrair informação útil dos oito pontos disponíveis.

No fim, ficou claro que projetar um sistema desse tipo é antes de tudo um exercício de prioridades. O suporte à vida vem primeiro, a transparência dos alertas vem em seguida, e a decisão final fica sempre com a tripulação. O software ajuda a olhar para muitos dados ao mesmo tempo, mas não substitui o julgamento humano.

## Estrutura do repositório

```
primeira-entrega2/
├── README.md
├── data/
│   ├── modulos_status.csv
│   ├── energia_leituras.csv
│   ├── variaveis_ambientais.csv
│   └── log_eventos.json
├── docs/
│   ├── relatorio.pdf
│   ├── link_video.txt
│   └── uso_ia.md
└── src/
    ├── main.py
    ├── config.py
    ├── dados.py
    ├── logica.py
    ├── previsao.py
    └── recomendacoes.py
```

