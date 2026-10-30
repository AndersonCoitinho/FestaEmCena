
import pandas as pd
import re


def limpar_categoria(valor):
    # Valores ausentes não têm categoria identificável.
    if pd.isna(valor):
        return "sem categoria"

    # Remover espaços externos e padronizar para minúsculas.
    valor = str(valor).strip().lower()

    # Remover pontuações, preservando letras e espaços.
    valor = re.sub(r"[^a-z ]", "", valor)

    # Remover espaços repetidos entre palavras.
    valor = " ".join(valor.split())

    # Se a limpeza deixar o campo vazio.
    if not valor:
        return "sem categoria"

    return valor


def limpar_canal(valor):
    if pd.isna(valor):
        return valor

    valor = str(valor).strip().lower()

    canais = {
        "mercado": "Mercado",
        "loja física": "Loja física",
        "web": "Web"
    }

    return canais.get(valor, valor)


def validar_quantidade(df):
    # Quantidade deve ser inteira e maior que zero.
    quantidade = pd.to_numeric(
        df["quantidade"], errors="coerce"
    )

    return (
        quantidade.isna() |
        (quantidade <= 0) |
        (quantidade % 1 != 0)
    )


def validar_preco(df):
    # Preço deve existir e não pode ser negativo.
    # Zero é permitido.
    preco = pd.to_numeric(
        df["preco_unitario"], errors="coerce"
    )

    return preco.isna() | (preco < 0)
