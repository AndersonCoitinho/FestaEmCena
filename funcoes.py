import pandas as pd
import re
from datetime import datetime

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

def verificar_entregas(df):

    # Considerar sem entrega quando a data estiver ausente (NaN) ou contiver apenas espaços.
    sem_entrega = (
        df["data_entrega"].isna() |
        df["data_entrega"].astype("string").str.strip().eq("").fillna(False)
    )

    cancelado = (
        df["status_pedido"]
        .astype("string")
        .str.strip()
        .str.lower()
        .eq("cancelado")
        .fillna(False)
    )

    # Separar os dois grupos.
    sem_entrega_cancelados = df[sem_entrega & cancelado]
    sem_entrega_outros = df[sem_entrega & ~cancelado]

    total_cancelados = len(sem_entrega_cancelados)
    total_outros = len(sem_entrega_outros)

    # Investigar a hipótese com condicionais.
    if total_outros > 0:
        print("Hipótese FALSA!")
        print("Existem pedidos sem entrega que não estão cancelados.")
    else:
        print("Hipótese VERDADEIRA nesta base!")

    print("Sem entrega e cancelados:", total_cancelados)
    print("Sem entrega e outros status:", total_outros)

    # Mostrar até três contraexemplos.
    if total_outros > 0:
        print("\nExemplos de pedidos:")
        print(
            sem_entrega_outros[
                ["pedido_id", "status_pedido", "data_entrega"]
            ].head(3)
        )


def converter_data(valor):
    # Se a data estiver vazia, retornamos None.
    if pd.isna(valor) or str(valor).strip() == "":
        return None

    try:
        # Converter texto para datetime no formato esperado.
        data = datetime.strptime(
            str(valor).strip(),
            "%Y-%m-%d %H:%M:%S"
        )

        return data

    except ValueError:
        # Se a data for inválida, o programa continua.
        return None
