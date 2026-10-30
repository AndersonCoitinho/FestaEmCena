import pandas as pd

df = pd.read_csv("halloween_vendas.csv")

# Categoria:
# Valores ausentes são preenchidos com "sem categoria", pois não é possível determinar a categoria verdadeira.
categoria_vazia = (
    df["categoria"].isna() |
    df["categoria"].astype("string").str.strip().eq("")
)

total_categoria_vazia = categoria_vazia.sum()
df.loc[categoria_vazia, "categoria"] = "sem categoria"

# Quantidade:
# Deve ser um número inteiro maior que zero, pois não faz sentido vender zero, quantidade negativa ou uma fração de unidade.
quantidade = pd.to_numeric(df["quantidade"], errors="coerce")

quantidade_invalida = (
    quantidade.isna() |
    (quantidade <= 0) |
    (quantidade % 1 != 0)
)

# Preço unitário:
# Deve estar preenchido e ser maior ou igual a zero. O valor zero é permitido, pois pode representar um produto gratuito.
preco = pd.to_numeric(df["preco_unitario"], errors="coerce")

preco_invalido = (
    preco.isna() |
    (preco < 0)
)

# Um pedido é marcado com problema se pelo menos uma das duas validações falhar.
df["com_problema"] = quantidade_invalida | preco_invalido

print("Categorias preenchidas:", total_categoria_vazia)
print("Quantidade inválida:", quantidade_invalida.sum())
print("Preço inválido:", preco_invalido.sum())

print("Total de pedidos afetados:",
      df.loc[df["com_problema"], "pedido_id"].nunique())