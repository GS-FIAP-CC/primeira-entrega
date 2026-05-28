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

**O que foi pedido:** geração de quatro arquivos CSV (`modulos.csv`, `energia.csv`, `ambiente.csv`, `log_eventos.csv`) seguindo os requisitos da Seção 7 do enunciado, com uma inconsistência proposital plantada para testar o sistema de diagnóstico.

**Prompt utilizado:**

```
Atue como engenheiro aeroespacial responsável pela telemetria de uma missão
espacial experimental. Gere um dataset simulando que será usado por um sistema
estudantil de monitoramento (Python, sem bibliotecas externas).

CENÁRIO
Escolha UM e mantenha coerência total em todo o dataset:
(a) Base de pesquisa em Marte: atmosfera fina, vento real, radiação alta
(b) Estação na superfície lunar: sem atmosfera, sem vento, radiação extrema
(c) Estação orbital experimental: microgravidade, exposição solar variável

Premissa narrativa: simule um turno de 12 a 24 horas em que a situação se
deteriora ao longo do tempo, gerando dados suficientes para o sistema
classificar estados normal, alerta e crítico.

DADOS OBRIGATÓRIOS

1 - Status binário de 6 módulos (1 = operacional, 0 = falha):
    suporte_vida, energia, comunicacao, habitat, laboratorio, armazenamento

2 - Telemetria energética MÍNIMO 6 horários ao longo do turno.
    Campos por linha: horario (HH:MM), geracao_solar_kwh, geracao_eolica_kwh,
    consumo_total_kwh, reserva_bateria_pct (0-100).
    A reserva deve evoluir de forma coerente: reserva_atual ≈ reserva_anterior
    + geracao_total - consumo. Geração solar = 0 à noite, picos próximos ao
    meio-dia. Geração eólica = 0 em cenários sem atmosfera.

3 - Variáveis ambientais (snapshot por horário OU único):
    temperatura_interna_c (habitável: 18-26), temperatura_externa_c (coerente
    com cenário), nivel_radiacao (baixa | media | alta | extrema),
    qualidade_comunicacao (boa | instavel | interrompida),
    velocidade_vento_ms (0 na Lua/órbita).

4 - Log de eventos MÍNIMO 8 registros, ordenados por timestamp.
    Campos: timestamp, tipo, modulo_afetado, descricao.
    Tipos válidos: ALERTA, FALHA_SENSOR, REINICIALIZACAO, MUDANCA_PRIORIDADE,
    MODO_ECONOMIA, INFO.
    Os eventos devem contar uma história com causa e efeito (ex.: queda na
    geração solar - modo economia - falha de sensor - reinicialização - alerta
    de comunicação instável).

5 - INCONSISTÊNCIA PROPOSITAL obrigatória, NÃO sinalizada.
    Insira UMA inconsistência plausível que a equipe precisará detectar.
    Exemplos válidos:
    - Módulo de comunicação marcado como 1 (operacional), mas log mostra falhas
      E qualidade_comunicacao está "interrompida"
    - Reserva de bateria aumenta entre dois horários sem geração que justifique
    - Temperatura interna reportada impossível com habitat marcado como normal
    Não comente qual é a inconsistência, ela deve ser descoberta pelo sistema.

REGRAS DE COERÊNCIA (críticas)
- Valores fisicamente plausíveis para o cenário escolhido
- Linha do tempo com causa e efeito (uma falha tem consequências nos próximos
  horários)
- Pelo menos 2 dos 6 módulos devem terminar em estado de alerta ou crítico,
  senão o sistema não terá o que analisar
- A inconsistência deve ser SUTIL mas detectável por verificação cruzada entre
  fontes (status x log x variável ambiental)

FORMATO DE SAÍDA
Entregue em 4 arquivos CSV separados (cabeçalho na primeira linha):
- modulos.csv: modulo, status
- energia.csv: horario, geracao_solar_kwh, geracao_eolica_kwh,
  consumo_total_kwh, reserva_bateria_pct
- ambiente.csv: timestamp, temperatura_interna_c, temperatura_externa_c,
  nivel_radiacao, qualidade_comunicacao, velocidade_vento_ms
- log_eventos.csv: timestamp, tipo, modulo_afetado, descricao

Ao final, escreva um parágrafo curto descrevendo a NARRATIVA que os dados
contam, mas SEM revelar onde está a inconsistência.
```

**Justificativa:** o enunciado autoriza explicitamente o uso de IA para gerar dados simulados.

### 1.2 [Adicionar outros usos se houver]

- **Ferramenta utilizada:**
- **O que foi pedido:**
- **O que NÃO foi pedido:**

### 1.3 [Adicionar outros usos se houver]

Exemplos possíveis (preencher apenas se ocorreram):

- Explicação de conceitos (ex.: como funciona média móvel)
- Revisão ortográfica/gramatical do relatório
- Sugestões de organização do código em funções
- Apoio na escrita do roteiro do vídeo

## 2. Onde a IA NÃO foi utilizada

Para deixar claro o que é trabalho original da equipe:

- **Código Python (`src/sistema.py`)** — escrito integralmente pela equipe, com base nos conceitos das Fases 1, 2 e 3
- **Lógica das regras de diagnóstico** — modeladas pela equipe a partir da interpretação dos dados
- **Escolha e justificativa das estruturas de dados** — decisão de projeto da equipe
- **Implementação da técnica de previsão** — implementada manualmente sem bibliotecas de ML
- **Análise dos resultados e conclusões do relatório** — reflexão crítica da equipe
- **Identificação da inconsistência no dataset** — descoberta por inspeção da equipe

## 3. Validação crítica realizada

Esta é a seção mais importante: o que a equipe conferiu e validou sobre o que a IA produziu.

### 3.1 Validação do dataset gerado

| Requisito do enunciado | Como validamos | Resultado |
|------------------------|----------------|-----------|
| 6 módulos críticos com status binário | Contagem manual em `modulos.csv` | OK |
| Mínimo 6 horários de leitura energética | Contagem de linhas em `energia.csv` | OK |
| Variáveis ambientais presentes | Inspeção de `ambiente.csv` | OK |
| Mínimo 8 registros de log | Contagem em `log_eventos.csv` | OK |
| Coerência física dos valores | Verificação de faixas (temperatura, radiação, vento) e da equação reserva ≈ reserva_anterior + geração - consumo | OK / [descrever ajustes feitos] |
| Coerência narrativa (causa e efeito) | Leitura cronológica do log cruzada com os horários energéticos | OK |
| Inconsistência proposital plantada | [Descrever qual era e como foi identificada] | OK |

**Inconsistência identificada pela equipe:**

> [Descrever aqui qual foi a inconsistência encontrada nos dados gerados pela IA. Ex.: "O módulo de comunicação aparece com status 1 em `modulos.csv`, mas o `log_eventos.csv` registra uma FALHA_SENSOR no módulo e `ambiente.csv` mostra qualidade_comunicacao como 'interrompida' a partir das 18:00. O sistema detectou essa contradição cruzando as três fontes."]

### 3.2 Validação do template de README

- A equipe conferiu se todas as 10 seções exigidas pelo enunciado (Seção 11) estavam presentes
- Cada placeholder foi substituído por conteúdo original da equipe — nenhum item ficou com texto genérico
- A tabela de estruturas de dados foi totalmente reescrita com base nas escolhas reais do projeto

### 3.3 Limitações observadas no uso de IA

Reflexão honesta da equipe sobre onde a IA falhou ou precisou de correção:

- [Ex.: "A primeira versão do dataset gerou geração solar > 0 durante a madrugada. Tivemos que pedir refinamento."]
- [Ex.: "A IA sugeriu uma inconsistência tão óbvia que ficamos sem desafio analítico. Pedimos uma versão mais sutil."]
- [Ex.: "O template de README inicial tinha sugestões de estruturas de dados que não fazem sentido para o problema. Substituímos."]

## 4. Reflexão final da equipe sobre o uso de IA

Esta seção deve ser escrita pela equipe, com base na experiência real. É um diferencial de avaliação demonstrar reflexão crítica sobre o uso da ferramenta.

**O que aprendemos sobre usar IA em projetos técnicos:**

- [Ex.: "Aprendemos que a IA é boa para acelerar tarefas repetitivas (gerar dados, formatar texto), mas a lógica de negócio precisa vir do humano que entende o problema."]
- [Ex.: "Percebemos que prompts vagos geram respostas genéricas — quanto mais específicos os requisitos, mais útil a resposta."]
- [Ex.: "A inconsistência plantada pela IA inicialmente foi grosseira; precisamos guiá-la para algo realmente sutil."]

**Quando NÃO usaríamos IA novamente:**

- [Ex.: "Para o código principal — escrever nós mesmos forçou a entender a fundo o que cada estrutura faz."]
- [Ex.: "Para as conclusões — a reflexão genuína só sai da experiência da equipe."]


*Documento elaborado pela equipe em conformidade com a Seção 13 do enunciado do Global Solution 1º Semestre 2026.*
