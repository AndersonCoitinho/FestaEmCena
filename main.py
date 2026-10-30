
import pandas as pd

from funcoes import (
    limpar_categoria,
    limpar_canal,
    validar_quantidade,
    validar_preco,
    verificar_entregas,
    converter_data
)


def main():
    # Ler CSV e armazenar em um DataFrame.
    df = pd.read_csv("halloween_vendas.csv")

    # Guardar valores originais para comparação.
    categoria_original = df["categoria"].copy()
    canal_original = df["canal_venda"].copy()

    # Identificar categorias originalmente vazias.
    # Também consideramos espaços e pontuações isoladas.
    categoria_limpa = categoria_original.apply(limpar_categoria)

    categorias_vazias = (
        categoria_limpa.eq("sem categoria") &
        (
            categoria_original.isna() |
            categoria_original.astype("string")
                .str.strip()
                .str.fullmatch(r"[^a-zA-Z]*").fillna(True)
        )
    )

    # Aplicar limpeza.
    df["categoria"] = categoria_limpa
    df["canal_venda"] = df["canal_venda"].apply(limpar_canal)

    # Contar alterações nas categorias não vazias.
    categorias_alteradas = (
        ~categorias_vazias &
        categoria_original.ne(df["categoria"]).fillna(False)
    )

    canais_alterados = (
        canal_original.ne(df["canal_venda"]).fillna(False)
    )

    # Validar quantidade e preço.
    quantidade_invalida = validar_quantidade(df)
    preco_invalido = validar_preco(df)

    # Marcar pedidos com pelo menos um problema.
    df["com_problema"] = (
        quantidade_invalida | preco_invalido
    )

    # Contar pedidos distintos para evitar duplicidade.
    pedidos_afetados = df.loc[
        df["com_problema"], "pedido_id"
    ].nunique()

    # Exibir resultados.
    print("Total de registros:", len(df))
    print("Categorias vazias preenchidas:", categorias_vazias.sum())
    print("Categorias não vazias alteradas:", categorias_alteradas.sum())
    print("Canais alterados:", canais_alterados.sum())
    print("Quantidades inválidas:", quantidade_invalida.sum())
    print("Preços inválidos:", preco_invalido.sum())
    print("Pedidos afetados:", pedidos_afetados)

    print("\n--- Verificação das entregas ---")
    verificar_entregas(df)

    
    df["data_venda_original"] = df["data_venda"].copy()

    # Converter as datas.
    df["data_convertida"] = df["data_venda"].apply(converter_data)

    # Marcar datas inválidas ou vazias.
    df["data_invalida"] = df["data_convertida"].isna()

    # Separar datas válidas e inválidas.
    datas_validas = df[~df["data_invalida"]]
    datas_invalidas = df[df["data_invalida"]]

    # Extrair ano, mês, dia e hora.
    df["ano"] = df["data_convertida"].apply(
        lambda data: data.year if pd.notna(data) else None
    )

    df["mes"] = df["data_convertida"].apply(
        lambda data: data.month if pd.notna(data) else None
    )

    df["dia"] = df["data_convertida"].apply(
        lambda data: data.day if pd.notna(data) else None
    )

    df["hora"] = df["data_convertida"].apply(
        lambda data: data.hour if pd.notna(data) else None
    )

    # Apresentar a data no formato brasileiro.
    df["data_brasileira"] = df["data_convertida"].apply(
        lambda data: data.strftime("%d/%m/%Y")
        if pd.notna(data) else None
    )

    # Mostrar resultados.
    print("\n--- Validação das datas ---")
    print("Datas válidas:", len(datas_validas))
    print("Datas inválidas ou vazias:", len(datas_invalidas))

    print("\nPrimeiras 5 datas:")
    print(df[[
        "data_venda_original",
        "ano",
        "mes",
        "dia",
        "hora",
        "data_brasileira"
    ]].head())



if __name__ == "__main__":
    main()
