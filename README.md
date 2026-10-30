1º Passo: Limpeza e validação dos dados  
Arquivo carregado  
Categoria: valores vazios foram substituídos por "sem categoria" <br>
Quantidade: deve ser um número inteiro maior que zero<br>
Preço unitario: deve estar preenchido e ser maior ou igual a zero

2º Passo: Padronização de Strings e Regex  
Padronizado da coluna categoria e canal_vendas

3º Passo: Logica de Regra de Negocio
Hipótese é falsa, pois existem 34 pedidos sem data de entrega que possuem status diferente de Cancelado.

4º Passo: Formatacao Temporal(Datetime)  
Convertido data_venda para o padrão brasileiro