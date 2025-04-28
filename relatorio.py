from google.cloud import bigquery
import pandas as pd
from datetime import datetime

def gerar_excel_precos(sku: list, canal: str):
    client = bigquery.Client()

    # Formata os SKUs corretamente para uso na query SQL
    if not sku:
        raise ValueError("Nenhum SKU foi fornecido.")
    skus_formatados = ",".join([f"'{s}'" for s in sku])

    query = f"""
        SELECT 
            sku_nike,
            nome_do_produto,
            ean,
            preco_de,
            preco_por
        FROM `crawlers-fisia.silver.cadastro_admin_full`
        WHERE sku_nike IN ({skus_formatados})
        AND preco_de IS NOT NULL
        ORDER BY sku_nike
    """

    produtos = client.query(query)
    df_produtos = produtos.to_dataframe()

    if df_produtos.empty:
        raise ValueError(f"⚠️ Nenhum produto encontrado para SKUs: {sku}")

    df_produtos["canal"] = canal
    df_produtos["action"] = "overwrite"
    df_produtos["ean"] = df_produtos["ean"].astype(str).str.split('.').str[0]
    df_produtos["preco_de"] = df_produtos["preco_de"].apply(lambda x: round(x, 2))
    df_produtos["preco_por_vigente"] = df_produtos["preco_por"].apply(lambda x: round(x, 2))
    df_produtos["preco_por"] = ''

    df_final = df_produtos[[
        "sku_nike", "nome_do_produto", "ean", "preco_de",
        "preco_por_vigente", "preco_por", "canal", "action"
    ]]

    df_final = df_final.rename(columns={
        "ean": "sku",
        "sku_nike": "cod_estilo",
        "nome_do_produto": "product_name",
        "canal": "pricetable_0_code",
        "action": "pricetable_0_action ( decrease, increase ou  overwrite)",
        "preco_de": "pricetable_0_price",
        "preco_por_vigente": "current_pricetable_0_special_price",
        "preco_por": "pricetable_0_special_price"
    })

    output_path = f"relatorio_produtos_{canal}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
    df_final.to_excel(output_path, index=False)
    return output_path
    