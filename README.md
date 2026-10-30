# Análise de Vendas de Halloween — Festa em Cena

## 1. Descrição do projeto

Este projeto foi desenvolvido para analisar os pedidos de Halloween da empresa fictícia Festa em Cena, utilizando Python.

O objetivo é realizar a leitura, limpeza, validação e análise dos registros de pedidos.

O programa utiliza bibliotecas como `csv`, `re`, `datetime` e `pandas`, aplicando conceitos de programação como funções, condicionais, laços de repetição, listas, dicionários e manipulação de arquivos CSV.

Os dados são fictícios e não representam necessariamente o comportamento do mercado real.

## 2. Estrutura dos dados

O arquivo `halloween_vendas.csv` contém 1.500 registros.

Cada linha representa um pedido registrado pela empresa.

Quatro colunas importantes são:

| Coluna | Descrição |
| `pedido_id` | Identificador do pedido |
| `categoria` | Categoria do produto, como fantasia ou acessório |
| `canal_venda` | Canal em que o pedido foi registrado |
| `data_venda` | Data e hora em que o pedido foi registrado |

Outros campos utilizados na análise incluem `quantidade`, `preco_unitario`, `status_pedido` e `data_entrega`.

É importante diferenciar a quantidade de pedidos da quantidade de unidades vendidas. As análises deste projeto contabilizam os registros de pedidos, não a soma das unidades de produtos.

## 3. Regras de limpeza e validação

### 3.1. Padronização das categorias

Foi realizada a normalização da coluna `categoria` utilizando `.strip()`, `.lower()` e `re.sub()`.

As regras utilizadas foram:

- Remover espaços no início e no final dos textos.
- Converter os textos para letras minúsculas.
- Remover pontuações e caracteres indevidos, preservando letras e espaços significativos.
- Remover espaços repetidos.
- Preencher categorias vazias com `"sem categoria"`.

A substituição por `"sem categoria"` foi escolhida porque não é possível determinar a categoria verdadeira de um registro com essa informação ausente.

Exemplos de transformação:

| Original | Padronizado |
|---|---|
| `FANTASIA!!!` | `fantasia` |
| ` Acessorio ` | `acessorio` |
| `FANTASIA` | `fantasia` |
| Valor vazio | `sem categoria` |

**Resultados:**

- Categorias vazias preenchidas: 18
- Categorias não vazias alteradas: 1.482

### 3.2. Padronização dos canais de venda

A coluna `canal_venda` foi padronizada para três valores:

- Mercado
- Loja física
- Web

Foram removidos espaços desnecessários e corrigidas diferenças de letras maiúsculas e minúsculas.

**Resultado:** 45 registros tiveram o canal de venda alterado durante a padronização.

### 3.3. Validação dos valores numéricos

Foram verificadas as colunas `quantidade` e `preco_unitario`.

**Quantidade:** deve ser um número inteiro maior que zero. Valores ausentes, negativos, iguais a zero ou não inteiros são considerados inválidos.

**Preço unitário:** deve estar preenchido e ser maior ou igual a zero. O valor zero é permitido, pois pode representar um produto gratuito, enquanto valores negativos são considerados inválidos.

Os registros com problemas foram marcados, sem inventar ou substituir os valores originais.

**Resultados:**

- Quantidades inválidas: 7
- Preços unitários inválidos: 12
- Pedidos distintos com problemas numéricos: 19

Foi utilizada uma condição lógica OU para identificar os pedidos com pelo menos um problema. A contagem de pedidos distintos evita que um mesmo pedido seja contabilizado duas vezes caso apresente múltiplas inconsistências.

### 3.4. Conversão e validação das datas

A coluna `data_venda` foi convertida utilizando `datetime.strptime()`, considerando o formato:

`%Y-%m-%d %H:%M:%S`

O texto original foi preservado, e foram extraídos:

- Ano
- Mês
- Dia
- Hora

Também foi criada uma apresentação no formato brasileiro por meio de `strftime("%d/%m/%Y")`.

Exemplo:

`2025-10-12 14:35:00` → `12/10/2025`

Datas inválidas ou vazias foram identificadas e marcadas, utilizando tratamento de exceções para permitir que o programa continuasse a execução.

Nenhuma data foi substituída pela data atual ou por valores fictícios.

**Resultados:**

- Datas válidas: 1.496
- Datas inválidas ou vazias: 4

## 4. Investigação das entregas

Foi investigada a seguinte hipótese:

**"Todos os pedidos sem data de entrega possuem status Cancelado."**

Para verificar essa hipótese, os registros com `data_entrega` vazia foram separados em dois grupos: pedidos cancelados e pedidos com outros status.

### Resultados

| Verificação | Quantidade |
|---|---:|
| Total de pedidos cancelados | 109 |
| Sem data de entrega e cancelados | 109 |
| Sem data de entrega com outros status | 34 |
| Total de pedidos sem data de entrega | 143 |

Foram encontrados os seguintes contraexemplos:

| Pedido ID | Status | Data de entrega |
|---|---|---|
| 1170 | Concluído | Vazia |
| 990 | Concluído | Vazia |
| 740 | Concluído | Vazia |

### Conclusão da hipótese

**A hipótese é falsa.**

Existem 34 pedidos sem data de entrega que possuem status diferente de Cancelado.

Portanto, não é correto afirmar que a ausência de data de entrega indica necessariamente que o pedido foi cancelado.

A análise foi realizada sem alterar os status ou preencher datas de entrega ausentes.

## 5. Análise por canal de venda

Os pedidos foram agrupados de acordo com o canal de venda, considerando todos os status.

| Canal | Pedidos | Participação |
|---|---:|---:|
| Web | 666 | 44,4% |
| Loja física | 551 | 36,7% |
| Mercado | 283 | 18,9% |
| **Total** | **1.500** | **100%** |

**Registros excluídos:** 0, pois todos os registros possuem um canal reconhecido após a padronização.

### Descoberta 1 — Canal com maior quantidade de pedidos

**Evidência numérica:** o canal Web registrou 666 pedidos, correspondendo a 44,4% dos 1.500 pedidos analisados.

**Interpretação:** entre os três canais, Web foi o que apresentou a maior quantidade de pedidos registrados, superando a Loja física e o Mercado.

**Limitação:** a contagem considera todos os status, inclusive cancelados e devolvidos. Dessa forma, os resultados representam pedidos registrados, não receita, unidades vendidas ou vendas efetivamente concluídas. Além disso, a base é fictícia e não permite generalizações sobre o mercado real.

## 6. Análise por período

Os pedidos foram agrupados por ano e mês da coluna `data_venda`, considerando apenas as datas válidas.

O agrupamento utiliza o formato `AAAA-MM`, evitando misturar meses de anos diferentes.

| Ano-mês | Pedidos |
|---|---:|
| 2024-08 | 77 |
| 2024-09 | 104 |
| 2024-10 | 393 |
| 2024-11 | 174 |
| 2025-08 | 62 |
| 2025-09 | 94 |
| 2025-10 | 410 |
| 2025-11 | 182 |
| **Total** | **1.496** |

**Registros excluídos:** 4, devido a datas de venda inválidas.

### Descoberta 2 — Período com maior quantidade de pedidos

**Evidência numérica:** outubro de 2025 apresentou 410 pedidos, enquanto outubro de 2024 apresentou 393, uma diferença de 17 pedidos.

**Interpretação:** outubro de 2025 foi o período com maior quantidade de pedidos registrados na base analisada.

**Limitação:** quatro pedidos foram excluídos dessa análise porque não possuem datas válidas. Além disso, a contagem inclui todos os status e não representa necessariamente vendas concluídas, faturamento ou comportamento geral do mercado.

## 7. Como executar o projeto

### Requisitos

- Python 3 instalado.
- Biblioteca Pandas instalada.
- Arquivos `main.py`, `funcoes.py` e `halloween_vendas.csv` na mesma pasta.

### Passo 1 — Abrir o projeto

Abra o VS Code e selecione a pasta do projeto.

### Passo 2 — Instalar a biblioteca Pandas

Abra o terminal e execute:

```bash
python -m pip install pandas
```

### Passo 3 — Executar o programa

No terminal, estando na pasta do projeto, execute:

```bash
python main.py
```

### Passo 4 — Conferir os resultados

O programa apresentará no terminal:

- Total de registros carregados.
- Contagens de categorias preenchidas e padronizadas.
- Quantidades e preços inválidos.
- Datas inválidas.
- Total de pedidos cancelados.
- Investigação da relação entre cancelamento e ausência de data de entrega.
- Contagem dos pedidos por canal e por ano-mês.
- Duas descobertas acompanhadas de interpretações e limitações.

O arquivo CSV original é utilizado somente para leitura, sem modificações.

## 8. Considerações finais

O projeto permitiu aplicar conceitos de programação em Python para realizar a leitura, limpeza, validação e análise de dados.

Foram identificadas inconsistências em categorias, quantidades, preços e datas, além de demonstrar que a ausência de data de entrega não significa necessariamente que o pedido foi cancelado.

As análises também permitiram identificar o canal com maior quantidade de pedidos registrados e o período com maior volume na base.

Os resultados são válidos apenas para o conjunto de dados fictício analisado e não devem ser interpretados como receita, volume de unidades vendidas ou comportamento do mercado real.