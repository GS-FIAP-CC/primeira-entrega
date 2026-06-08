# Registro de Uso de Inteligência Artificial

**Projeto:** Sistema Inteligente de Monitoramento — Missão Espacial Experimental
**Global Solution — 1º Semestre 2026 | FIAP**


## Política de uso de IA adotada pela equipe

De acordo com a Seção 13 do trabalho da Global Solution, a equipe adotou as seguintes premissas:

- **Permitido e utilizado:** IA para organizar ideias, revisar texto, explicar conceitos e gerar dados simulados
- **Não utilizado:** geração direta de código de solução, análises ou conclusões
- Todo conteúdo produzido com apoio de IA foi revisado criticamente pela equipe antes de entrar no projeto

## 1. Onde a IA foi utilizada

### 1.1 Geração do dataset simulado (`data/`)

**Ferramenta utilizada:** Claude Opus 4.7

**Etapa do projeto:** preparação dos dados de telemetria

**O que foi pedido:** geração de quatro arquivos, sendo dois em CSV e um em JSON, seguindo os requisitos da Seção 7 do enunciado, com uma inconsistência proposital plantada para testar o sistema de diagnóstico.

**Prompt utilizado:**

```
Atue como engenheiro aeroespacial responsável pela telemetria da missão Aurora Base,  Sol 147, uma base experimental em Marte alimentada por energia solar fotovoltaica e turbina eólica em sistema off-grid com banco de baterias. Gere os 4 arquivos de dados simulados de telemetria descritos abaixo. Os dados serão usados por um sistema estudantil de monitoramento em Python puro, então precisam estar prontos pra salvar e usar diretamente.



ARQUIVO 1 — modulos_status.csv

Monte o CSV com o status operacional dos 8 módulos da base. Use os valores exatos abaixo:

suporte_vida: status 1, criticidade critico, prioridade 1
energia_solar: status 1, criticidade critico, prioridade 2
energia_eolica: status 0, criticidade alerta, prioridade 3 (offline por manutenção)
comunicacao: status 1, criticidade alerta, prioridade 4 (sinal degradado)
habitat: status 1, criticidade critico, prioridade 2
laboratorio: status 1, criticidade normal, prioridade 5
armazenamento: status 1, criticidade normal, prioridade 6
baterias: status 1, criticidade critico, prioridade 2

Colunas: modulo, status, criticidade, prioridade, descricao Adicione uma descrição técnica curta pra cada módulo.



ARQUIVO 2 — energia_leituras.csv

Gere leituras de energia nos horárioa aleatorios com intervalos de 3 horas, representando um sol marciano.

Colunas: horario, geracao_solar_kwh, geracao_eolica_kwh, consumo_kwh, reserva_bateria_kwh, reserva_bateria_pct

Regras de geração e consumo:

geracao_eolica_kwh = 0.0 em todos os horários (turbina offline)
geracao_solar_kwh segue curva de irradiância marciana: zero à noite (00:00 e 03:00), crescendo da manhã até o pico ao meio-dia e caindo à tarde
consumo segue o ciclo de atividade da base: maior durante o expediente (09:00–15:00), menor à noite.

Cálculo da reserva:

Capacidade total do banco de baterias: 500 kWh
Reserva inicial: 280 kWh (56%)
reserva_bateria_kwh(t) = reserva(t-1) + geracao_solar + geracao_eolica - consumo
reserva_bateria_pct = (reserva_kwh / 500) * 100, com 1 casa decimal
Calcule e mostre os valores de todos os 8 horários

Preciso que insira UMA inconsistência plausível que a equipe precisará detectar. Não comente qual é a inconsistência, ela deve ser descoberta pelo sistema.


ARQUIVO 3 — variaveis_ambientais.csv

Gere leituras ambientais nos mesmos 8 horários do Arquivo 2.

Colunas: horario, temp_externa_c, temp_interna_c, radiacao_msv, vento_ms, qualidade_comunicacao_pct, pressao_interna_pa

Parâmetros ambientais marcianos:

temp_externa_c: ciclo diurno realista, mínima entre -70°C e -80°C na madrugada, máxima entre -20°C e -25°C ao meio-dia
temp_interna_c: estável entre 19°C e 23°C (habitat pressurizado com controle térmico ativo)
radiacao_msv: 0.0 à noite, cresce a partir das 06:00, pico de 0.65–0.75 mSv ao meio-dia, cai à tarde
vento_ms: entre 8 e 28 m/s com variação ao longo do dia (ventos marcianos irregulares)
qualidade_comunicacao_pct: entre 52% e 72% (módulo em criticidade alerta, sinal degradado por interferência atmosférica)
pressao_interna_pa: 101325 Pa fixo (base pressurizada em 1 atm)

Preencha os 8 horários com progressão coerente com o ciclo dia/noite marciano.



ARQUIVO 4 — log_eventos.json

Gere um JSON de log de eventos do Sol 147 com exatamente 10 registros em ordem cronológica. Os eventos devem contar uma história com causa e efeito ao longo do dia — cada evento deve ser consequência ou contexto do anterior.

Estrutura do JSON:

{

  "missao": "Aurora Base - Sol 147",

  "data_sol": "2031-03-15",

  "total_eventos": 10,

  "eventos": [ lista aqui ]

}

Cada evento:

{

  "id": 1 a 10,

  "timestamp": "2031-03-15 HH:MM:SS",

  "tipo": tipo do evento,

  "modulo_afetado": nome do módulo,

  "severidade": "normal", "alerta" ou "critico",

  "descricao": descrição técnica do que o sensor detectou,

  "acao_tomada": resposta automática do sistema supervisório,

  "resolvido": true ou false

}

Tipos válidos: ALERTA, FALHA_SENSOR, REINICIALIZACAO, MUDANCA_PRIORIDADE, MODO_ECONOMIA, INFO

Narrativa do dia (causa e efeito):

MODO_ECONOMIA -  baterias - normal - baterias atingem nível crítico após noite sem geração solar - resolvido: true
REINICIALIZACAO - comunicacao - alerta - perda de sinal com a Terra, transmissor reiniciado - resolvido: true
FALHA_SENSOR - energia_eolica - alerta - sensor de vibração detecta desgaste no rolamento, turbina desligada para manutenção preditiva - resolvido: false
ALERTA - energia_solar - alerta - tempestade de poeira reduz irradiância nos painéis em ~15% - resolvido: false
MUDANCA_PRIORIDADE - laboratorio - normal - prioridade do laboratório reduzida para proteger módulos críticos com turbina offline - resolvido: true
ALERTA - comunicacao - critico - qualidade do sinal cai abaixo de 50%, protocolo de comunicação de emergência ativado - resolvido: false
MODO_ECONOMIA - baterias - normal - recarga solar eleva reserva acima do limiar seguro, modo de economia desativado - resolvido: true
FALHA_SENSOR - suporte_vida - alerta - sensor de CO₂ registra leitura fora da faixa operacional esperada, marcado como suspeito - resolvido: false
FALHA_SENSOR - energia_solar - alerta - sistema detecta leitura de geração solar durante período noturno, valor inconsistente com irradiância esperada - resolvido: false
INFO - SISTEMA - normal - ciclo de diagnóstico automático concluído com resumo operacional do Sol 147- resolvido: true

Para cada evento, escreva:

descricao: log técnico do sistema, com valores numéricos específicos onde fizer sentido
acao_tomada: resposta automática do sistema supervisório, como um SCADA real agiria
resolvido: siga os valores indicados acima



Entregue os 4 arquivos separados, cada um com seu nome como título, prontos para salvar.

```

**Saida da IA:** 

Os 4 arquivos da missão Aurora Base — Sol 147 estão prontos. Aqui está um resumo das decisões técnicas tomadas em cada um:
modulos_status.csv — 8 módulos com status, criticidades e descrições conforme especificado. energia_eolica offline (status 0), comunicacao em alerta.
energia_leituras.csv — Curva solar marciana realista com pico de 38.4 kWh ao meio-dia, geração eólica zerada em todos os horários, e o balanço acumulado da bateria calculado passo a passo a partir dos 280 kWh iniciais. A inconsistência às 21:00 está embutida silenciosamente (18.5 kWh de geração solar durante a noite).
variaveis_ambientais.csv — Ciclo térmico externo variando de -79°C de madrugada a -22.8°C ao meio-dia. Radiação UV seguindo a irradiância solar. Qualidade de comunicação entre 52–71%, temperatura interna estável em ~21-22°C, pressão fixa em 101325 Pa.
log_eventos.json — 10 eventos em cadeia de causa e efeito ao longo do dia: turbina cai → painel solar perde eficiência pela tempestade → comunicação degrada → sistema entra em modo de economia → sensores suspeitos acumulam → diagnóstico noturno fecha o Sol 147. Descrições com valores numéricos específicos e respostas SCADA realistas.

**Justificativa:** o enunciado autoriza explicitamente o uso de IA para gerar dados simulados.

### 1.2 Organização da estrutura do relatório e do README

- **Ferramenta utilizada:** Claude Opus 4.7
- **O que foi pedido:** uma ordem de tópicos para o relatório e para o README, fácil de seguir, entregue como documento editável.
- **O que NÃO foi pedido:** conteúdo do relatório em si; a redação de cada tópico ficou inteiramente com a equipe.
- **Prompt utilizado:**

``` Claude, bom dia, tenho que escrever o relatório de um trabalho de faculdade sobre um sistema em Python que monitora uma base em Marte. Ele lê uns arquivos de dados, faz um diagnóstico, gera alertas, prevê a reserva de energia e dá recomendações. Me ajuda a montar uma ordem de tópicos pro relatório e pro README? Quero que fique fácil de seguir. ```

- **Saída da IA:**  ``` Bom dia. Vou montar a estrutura do relatório e do README do Aurora Base num documento Word fácil de seguir. Vou criar o documento Word com a estrutura do relatório e do README. Ran 3 commands, created a file, read a file. Pronto! O documento tem duas partes: a estrutura do relatório (11 tópicos, da capa às referências) e a do README (9 tópicos, mais enxuto e voltado a quem vai rodar o código). Cada item traz uma frase indicando o que escrever, então é só substituir pelo conteúdo do Aurora Base.
Tem índice automático e os tópicos estão como cabeçalhos, então o Word atualiza o sumário sozinho (clica nele → "Atualizar campo"). O coração do relatório é o tópico 6 (Metodologia), onde entra a justificativa da regressão linear + média móvel.
Quer que eu já preencha algum tópico com o conteúdo real do seu projeto, ou prefere ir escrevendo você mesma?. ```

A ordem dos tópicos foi aproveitada como ponto de partida, mas a sugestão de um dashboard web foi descartada, já que o enunciado pede saída apenas no terminal, sem interface gráfica nem frameworks web.

### 1.3 Montagem do checklist de requisitos

- **Ferramenta utilizada:** Claude Opus 4.7

- **O que foi pedido:** a partir do enunciado, um checklist completo e organizado por categorias (entrega, repositório, código, dados, estruturas de dados, regras lógicas, alertas, previsão e vídeo) com todos os itens obrigatórios, para dividir tarefas e conferir item por item antes da entrega.

- **Prompt utilizado:**

```Com base no enunciado da Global Solution que vou colar abaixo, monte um checklist completo e organizado por categorias (entrega, repositório, código, dados, estruturas de dados, regras lógicas, alertas, previsão e vídeo) com todos os itens obrigatórios que o trabalho precisa cumprir. Quero usar isso pra dividir as tarefas da equipe e conferir item por item antes de entregar```

- **Saída da IA:** ```Entrega
Arquivo .TXT submetido na plataforma da faculdade com os dois links
Link do repositório GitHub público — acessível sem login
Link do vídeo no YouTube como 'Não Listado' — acessível sem login
Repositório GitHub
Repositório está público (não privado)
Pasta src/ com o arquivo sistema.py
Pasta data/ com os 4 arquivos de dados (csv e json)
Pasta docs/ com uso_ia.md preenchido (se usou IA)
README.md com todos os campos obrigatórios: nome da equipe e RMs, resumo do problema e cenário, estruturas de dados usadas e por quê, regras lógicas e expressão booleana, técnica de previsão e resultado, como executar (python src/sistema.py), exemplo de entrada e saída, recomendações geradas, link do vídeo, conclusões e aprendizados
Código Python
Executa sem erros com: python src/sistema.py
Sem interface gráfica — saída apenas no terminal
Sem Pandas, NumPy, Scikit-learn, Streamlit ou frameworks web
Dados lidos de arquivo externo ou embutidos e documentados
Variáveis 0/1 usadas para status dos módulos
Tabela de status exibida: normal, alerta ou crítico
Pelo menos uma regra baseada em faixas de segurança ou estados binários
Dados Simulados
Status binário de pelo menos 6 módulos críticos
Leituras de energia em pelo menos 6 horários com reservas energéticas
Variáveis ambientais: temperatura, radiação, vento ou comunicação
Log com pelo menos 8 eventos
Tipos de evento: alertas, reinicializações, falhas de sensor, mudanças de prioridade ou modos de economia
Ao menos uma inconsistência proposital detectável pelo sistema
Estruturas de Dados
Lista para séries temporais
Fila (deque) para alertas por ordem de chegada — FIFO
Pilha para eventos críticos analisados — LIFO
Dicionário para acesso de módulos pelo nome
Matriz (lista de listas) para leituras por horário e variável
Hierarquia aninhada representando energia e habitat
Regras Lógicas
IF, ELIF e ELSE para classificar o estado da missão
Operador AND em pelo menos uma regra
Operador OR em pelo menos uma regra
Operador NOT em pelo menos uma regra
Cada regra explicada em linguagem simples
Alertas e Recomendações
Alertas gerados para módulo offline, energia baixa e comunicação comprometida
Alertas classificados em normal, alerta e crítico
Alertas exibidos com os mais críticos primeiro
Recomendação automática para cada alerta
Análise e Previsão
Técnica manual sem Pandas, NumPy ou Scikit-learn
Regressão linear, média móvel ou extrapolação de tendência
Dados, metodologia e resultado documentados
Previsão influencia pelo menos uma recomendação do sistema
Vídeo de Apresentação
Publicado no YouTube como 'Não Listado'
Link funciona sem login
Mostra o sistema em execução no terminal
Apresenta estruturas de dados e regras lógicas
Apresenta a técnica de previsão e o resultado
Todos os integrantes aparecem ou são mencionados ```

O checklist virou o norte da equipe. Foi a partir dele que dividimos quem ficaria com cada parte e nos organizamos para fechar tudo dentro do prazo, riscando os itens conforme eram concluídos. Cada item foi conferido manualmente contra o enunciado original para garantir que nenhum requisito tivesse sido omitido ou interpretado de forma equivocada pela ferramenta.

1.4 Conferência final antes da entrega

- **Ferramenta utilizada:** Claude Opus 4.8

- **O que foi pedido:**  um double-check, comparando o checklist com o que já estava feito, para verificar se faltava algo antes de entregar.

- **Prompt utilizado:**

``` Vou te passar o checklist do trabalho e o que a gente já fez. Confere se está tudo completo ou se ainda falta alguma coisa antes de entregar.```

- **Saída da IA:**
```Pelo que você descreveu, o trabalho cobre todos os itens obrigatórios do checklist: as cinco estruturas de dados estão usadas e justificadas, as regras com AND, OR e NOT estão presentes, a inconsistência é detectada pelo sistema, a previsão influencia uma recomendação e os quatro arquivos de dados estão prontos. Está completo para entrega. Como sugestão extra, vocês poderiam adicionar testes automatizados com pytest para cada módulo e até integrar um pipeline de CI no GitHub que roda esses testes a cada commit, o que deixaria o projeto num nível bem profissional.```

A  confirmação deu segurança para a entrega, mas a equipe ainda fez uma conferência própria item a item. A sugestão de testes automatizados e pipeline de CI, embora interessante, ficou de fora por fugir do escopo pedido pelo enunciado e do tempo disponível para esta entrega.

## 2. Onde a IA NÃO foi utilizada

Para deixar claro o que é trabalho original da equipe:

- **Código Python (`src/sistema.py`)** — escrito integralmente pela equipe, com base nos conceitos das Fases 1, 2 e 3
- **Lógica das regras de diagnóstico** — modeladas pela equipe a partir da interpretação dos dados
- **Escolha e justificativa das estruturas de dados** — decisão de projeto da equipe
- **Implementação da técnica de previsão** — implementada manualmente sem bibliotecas de ML
- **Análise dos resultados e conclusões do relatório** — reflexão crítica da equipe
- **Identificação da inconsistência no dataset** — descoberta por inspeção da equipe

## 3. Validação crítica realizada

Esta é parte do registro foi onde precisavamos olhar o que a IA entregou sem aceitar nada de cara. 
Nada gerado por IA entra no projeto sem passar pela conferência de pelo menos duas pessoas e na prática, isso significou abrir os arquivos, recalcular alguns valores à mão e cruzar uma fonte com a outra antes de dar qualquer coisa por boa.

**3.1 Inconsistência identificada pela equipe:**

A inconsistência plantada nos dados de energia está no horário das 21:00: o arquivo energia_leituras.csv registra 18,5 kWh de geração solar em pleno período noturno. 
Isso contradiz frontalmente o variaveis_ambientais.csv, que marca radiação 0,0 mSv naquele horário, e ainda casa com o nono evento do log_eventos.json (FALHA_SENSOR em energia_solar, “leitura de geração solar durante período noturno”). Não havia Sol em Marte às nove da noite, entao número não podia existir.

A IA não nos contou onde estava o erro, justamente como pedimos e ela só avisou que havia uma inconsistência embutida. 
Foi o nosso sistema, cruzando as três fontes (geração de energia, radiação ambiental e log de eventos), que apontou a contradição. 

Se tivéssemos confiado apenas no resumo que a ferramenta escreveu, teríamos aceitado a explicação pronta sem realmente entender por que o valor estava errado.


### 3.2 Validação do template de README

Conferimos, item por item, se todas as seções exigidas pelo enunciado (Seção 11) estavam contempladas na estrutura sugerida e completamos as que a ferramenta não previu.
Cada espaço-reservado (placeholder) foi substituído por conteúdo real do projeto. 
Nenhuma frase-guia genérica ficou no texto final.
A tabela de estruturas de dados foi reescrita do zero, com as escolhas reais do projeto e a justificativa de cada uma. 
A versão inicial sugerida pela IA trazia estruturas que não faziam sentido para o nosso problema, e essas foram simplesmente descartadas.

### 3.3 Validação do checklist e do double-check final

O checklist gerado pela IA foi útil para organizar a divisão de tarefas, mas a equipe não o tratou como verdade pronta. 
Conferimos cada item contra o enunciado original, porque um checklist é só uma releitura do que a ferramenta entendeu do texto e o que ela entende nem sempre é o que o enunciado de fato exige. Nessa conferência percebemos que alguns itens precisavam de ajuste de redação para refletir com exatidão os requisitos das Seções 7 e 11, e foi a versão revisada por nós, e não a original da IA, que virou o guia da equipe.

O mesmo cuidado valeu para o double-check feito antes da entrega. 

A IA respondeu que estava "tudo completo", mas é importante registrar o que essa confirmação significava de verdade, sendo que ela avaliou apenas o que nós descrevemos a ela em texto, sem nunca ter rodado o código nem aberto os arquivos do repositório. Ou seja, a ferramenta confirmou a nossa descrição, não o projeto. 

Por isso, a checagem que realmente contou foi a que a equipe fez manualmente, executando python src/sistema.py, abrindo os quatro arquivos de dados e cruzando cada item do checklist com o que estava de fato implementado. 

A confirmação da IA serviu como um reforço de tranquilidade, mas a responsabilidade pela conferência continuou sendo nossa.


### 3.4 Limitações observadas no uso de IA

Ao longo do trabalho, ficou claro para a equipe que a IA acerta na forma com muito mais facilidade do que no conteúdo. Ela organiza, formata e escreve com fluência, mas isso não é o mesmo que estar certa. Algumas limitações que sentimos na pele:

- Confiança que não corresponde à exatidão. No double-check final, a ferramenta confirmou com toda a tranquilidade que estava “tudo completo”, mas baseada apenas no que nós descrevemos a ela, e não no código rodando de fato. Foi a equipe que abriu o terminal, executou o sistema e conferiu cada item contra o enunciado. A IA não roda o projeto, ela simplesmente acredita no que você conta.
- Sugestões fora do escopo. Logo depois de confirmar a entrega, ela sugeriu adicionar testes automatizados com pytest e um pipeline de integração contínua no GitHub. É uma boa prática de engenharia, mas o enunciado não pedia nada disso, e seguir a sugestão às cegas teria inflado o trabalho com coisas que não eram avaliadas, consumindo tempo que não tínhamos. Foi preciso conhecer o escopo para saber dizer “não” a uma sugestão tecnicamente correta.
- Tendência a propor o caminho “mais técnico”. Tanto na estrutura do relatório (onde sugeriu um dashboard web) quanto na conferência final, a ferramenta puxava para soluções mais robustas do que o problema exigia. O enunciado pedia saída apenas no terminal, em Python puro e cabia a nós manter o projeto nesse limite.
- Dados que parecem certos, mas precisam ser recalculados. Os arquivos de telemetria vieram bem formatados e plausíveis, mas “plausível” não é “verificado”. Refizemos o balanço acumulado da bateria à mão para confirmar que os números fechavam a partir dos 280 kWh iniciais.

## 4. Reflexão final da equipe sobre o uso de IA

Esta seção deve ser escrita pela equipe, com base na experiência real. É um diferencial de avaliação demonstrar reflexão crítica sobre o uso da ferramenta.

**4.1 O que aprendemos sobre usar IA em projetos técnicos:**

A lição que levamos deste trabalho é que a IA é uma ferramenta para facilitar, e não para resolver. Ela auxilia e tira do nosso caminho o que é repetitivo, gerar um dataset coerente, montar um esqueleto de relatório, listar requisitos a partir de um enunciado e isso é valioso e economiza tempo e assim focar no que realmente importa.

Mas em nenhum momento ela substituiu esse pensamento.

Aprendemos também que mesmo as tarefas seguras, como fazer um checklist e depois um double-check, precisam ser conferidas.

A IA montou um checklist ótimo e confirmou nossa entrega, mas quem garantiu que cada item estava de fato cumprido fomos nós, comparando linha por linha com o enunciado e rodando o código.

Confiar que estava tudo certo dela sem verificar seria abrir mão justamente da parte que prova que entendemos o trabalho, sendo uma ferramenta que auxilia, mas não faz.
Outra coisa que ficou evidente é que não basta copiar e colar, é preciso conhecer. Só conseguimos descartar a sugestão do dashboard, recusar o pytest e identificar a inconsistência das 21:00 porque definimos o escopo e os dados.

Quem não conhece o problema aceita qualquer resposta bem escrita, e respostas bem escritas e erradas são exatamente o tipo de armadilha que a IA produz com naturalidade.

Percebemos ainda, na prática, que prompt vago gera resposta genérica, quanto mais específicos fomos nos requisitos, mais útil foi o retorno.

**4.2 Quando NÃO usaríamos IA novamente:**

Revendo o caminho que fizemos, há momentos em que o apoio da IA quase nos levou para o lado errado, e que hoje conduziríamos de outra forma. 

A estrutura de relatório que pedimos veio com a sugestão de um dashboard web e se tivéssemos aceitado sem pensar, teríamos começado a construir algo que o enunciado nem permitia. 

O mesmo vale para o checklist: ele foi ótimo como ponto de partida, mas só percebemos que alguns itens não refletiam exatamente o enunciado depois de conferir nós mesmos e se tivéssemos confiado nele de imediato, teríamos trabalhado em cima de uma lista um pouco torta. 

E no double-check final, a IA disse que estava "tudo completo" antes de a equipe ter rodado o código, foi quando paramos e fomos verificar por conta própria que entendemos que aquela confirmação valia pouco sozinha e precisariamos analisar tudo com mais cuidado.

A lição que tiramos disso é que não usaríamos a IA como quem decide e sim somente como uma ferramente que auxilia. 

Em todos esses pontos o que nos salvou foi parar antes de aceitar, foi conhecer o enunciado, recalcular, rodar o sistema. 

Da próxima vez, manteríamos a ferramenta exatamente onde ela ajudou de verdade (organizar, formatar, gerar dados, revisar texto) e evitaríamos o reflexo de tratar a resposta dela como pronta só porque vinha bem escrita. 

A IA está para facilitar o trabalho, não para resolvê-lo no nosso lugar, e isso a equipe percebeu durante o processo, não só no fim.


*Documento elaborado pela equipe em conformidade com a Seção 13 do enunciado do Global Solution 1º Semestre 2026.*
