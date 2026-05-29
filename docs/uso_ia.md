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
