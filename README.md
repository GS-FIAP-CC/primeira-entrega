
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


## Técnica de previsão


## Como executar


## Exemplo de entrada e saída


## Recomendações geradas pelo sistema


## Link do vídeo


## Conclusões e aprendizados


## Estrutura do repositório


