# from google.cloud import bigquery
# import pandas as pd
# from datetime import datetime

# def gerar_excel_precos(sku: list, canal: str):
#     client = bigquery.Client()

#     # Formata os SKUs corretamente para uso na query SQL
#     if not sku:
#         raise ValueError("Nenhum SKU foi fornecido.")
#     skus_formatados = ",".join([f"'{s}'" for s in sku])
#     query = f"""
#         SELECT 
#             sku_nike,
#             nome_do_produto,
#             ean,
#             preco_de,
#             preco_por
#         FROM `crawlers-fisia.silver.cadastro_admin_full`
#         WHERE sku_nike IN ({skus_formatados})
#         AND preco_de IS NOT NULL
#         ORDER BY sku_nike
#     """

#     produtos = client.query(query)
#     df_produtos = produtos.to_dataframe()

#     if df_produtos.empty:
#         raise ValueError(f"⚠️ Nenhum produto encontrado para SKUs: {sku}")
    
#     df_produtos["ean"] = df_produtos["ean"].astype(str).str.split('.').str[0]
#     df_produtos["preco_de"] = df_produtos["preco_de"].apply(lambda x: round(x, 2))
#     df_produtos["preco_por"] = ''
#     df_produtos["canal"] = canal
#     df_produtos["action"] = "overwrite"
#     df_produtos["pricetable_0_price"] = ''
#     df_produtos["pricetable_0_special_price"] = ''
#     df_produtos["pricetable_0_percentage"] = ''

#     df_final = df_produtos[[
#         "ean","preco_de","preco_por","sku_nike","canal","action", 
#         "nome_do_produto", "sku_nike"  
#     ]]

#     df_final = df_final.rename(columns={
#         "ean": "sku",
#         "preco_de": "price",
#         "preco_por": "special_price",
#         "canal": "pricetable_0_code",
#         "action": "pricetable_0_action ( decrease, increase ou  overwrite)",
#         "sku_nike": "cod_estilo",
#         "nome_do_produto": "product_name",
#     })

#     output_path = f"relatorio_produtos_{canal}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
#     df_final.to_excel(output_path, index=False)
#     return output_path

# from google.cloud import bigquery
# import pandas as pd
# from datetime import datetime

# def gerar_excel_precos(sku: list, canal: str):
#     client = bigquery.Client()

#     if not sku:
#         raise ValueError("Nenhum SKU foi fornecido.")

#     skus_formatados = ",".join([f"'{s}'" for s in sku])
#     query = f"""
#         SELECT 
#             sku_nike,
#             nome_do_produto,
#             ean,
#             preco_de
#         FROM `crawlers-fisia.silver.cadastro_admin_full`
#         WHERE sku_nike IN ({skus_formatados})
#         AND preco_de IS NOT NULL
#         ORDER BY sku_nike
#     """

#     produtos = client.query(query)
#     df = produtos.to_dataframe()

#     if df.empty:
#         raise ValueError(f"⚠️ Nenhum produto encontrado para SKUs: {sku}")

#     df["sku"] = df["ean"].astype(str).str.split(".").str[0]
#     df["price"] = df["preco_de"].apply(lambda x: round(x, 2))
#     df["special_price"] = ""
#     df["cod_estilo"] = df["sku_nike"]
#     df["pricetable_0_code"] = canal
#     df["pricetable_0_action ( decrease, increase ou  overwrite)"] = "overwrite"
#     df["product_name"] = df["nome_do_produto"]

#     df["pricetable_0_price"] = ""
#     df["pricetable_0_special_price"] = ""
#     df["pricetable_0_percentage"] = ""

#     df["pricetable_1_code"] = ""
#     df["pricetable_1_action  ( decrease, increase ou  overwrite)"] = ""
#     df["pricetable_1_price"] = ""
#     df["pricetable_1_special_price"] = ""
#     df["pricetable_1_percentage"] = ""

#     df["pricetable_2_code"] = ""
#     df["pricetable_2_action"] = ""
#     df["pricetable_2_price"] = ""
#     df["pricetable_2_special_price"] = ""
#     df["pricetable_2_percentage"] = ""

#     colunas_ordenadas = [
#         "sku", "price", "special_price", "cod_estilo", "pricetable_0_code",
#         "pricetable_0_action ( decrease, increase ou  overwrite)", "product_name",
#         "pricetable_0_price", "pricetable_0_special_price", "pricetable_0_percentage",
#         "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
#         "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
#         "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
#         "pricetable_2_special_price", "pricetable_2_percentage"
#     ]

#     df_final = df[colunas_ordenadas]

#     output_path = f"relatorio_produtos_{canal}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
#     df_final.to_excel(output_path, index=False)
#     return output_path
# from google.cloud import bigquery
# import pandas as pd
# from datetime import datetime

# def gerar_excel_precos(sku: list, canal: str):
#     client = bigquery.Client()

#     if not sku:
#         raise ValueError("Nenhum SKU foi fornecido.")

#     skus_formatados = ",".join([f"'{s}'" for s in sku])
#     query = f"""
#         SELECT 
#             sku_nike,
#             nome_do_produto,
#             ean,
#             preco_de
#         FROM `crawlers-fisia.silver.cadastro_admin_full`
#         WHERE sku_nike IN ({skus_formatados})
#         ORDER BY sku_nike
#     """

#     produtos = client.query(query)
#     df = produtos.to_dataframe()

#     if df.empty:
#         raise ValueError(f"⚠️ Nenhum produto encontrado para SKUs: {sku}")

#     df["ean"] = df["ean"].astype(str).str.split('.').str[0]
#     df["preco_de"] = df["preco_de"].apply(lambda x: round(x, 2) if pd.notnull(x) else '')
#     df["special_price"] = ''
#     df["cod_estilo"] = df["sku_nike"]
#     df["pricetable_0_code"] = canal
#     df["pricetable_0_action ( decrease, increase ou  overwrite)"] = "overwrite"
#     df["product_name"] = df["nome_do_produto"]
#     df["pricetable_0_price"] = ''
#     df["pricetable_0_special_price"] = ''
#     df["pricetable_0_percentage"] = ''
#     df["pricetable_1_code"] = ''
#     df["pricetable_1_action  ( decrease, increase ou  overwrite)"] = ''
#     df["pricetable_1_price"] = ''
#     df["pricetable_1_special_price"] = ''
#     df["pricetable_1_percentage"] = ''
#     df["pricetable_2_code"] = ''
#     df["pricetable_2_action"] = ''
#     df["pricetable_2_price"] = ''
#     df["pricetable_2_special_price"] = ''
#     df["pricetable_2_percentage"] = ''

#     df_final = df[[  # ordem desejada
#         "ean", "preco_de", "special_price", "cod_estilo",
#         "pricetable_0_code", "pricetable_0_action ( decrease, increase ou  overwrite)",
#         "product_name", "pricetable_0_price", "pricetable_0_special_price", "pricetable_0_percentage",
#         "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
#         "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
#         "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
#         "pricetable_2_special_price", "pricetable_2_percentage"
#     ]].rename(columns={
#         "ean": "sku",
#         "preco_de": "price"
#     })

#     output_path = f"relatorio_produtos_{canal}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
#     df_final.to_excel(output_path, index=False)
#     return output_path

# from google.cloud import bigquery
# import pandas as pd
# from datetime import datetime

# def gerar_excel_precos(sku: list, canal: str):
#     client = bigquery.Client()

#     if not sku:
#         raise ValueError("Nenhum SKU foi fornecido.")

#     skus_formatados = ",".join([f"'{s}'" for s in sku])
#     query = f"""
#         SELECT 
#             sku_nike,
#             nome_do_produto,
#             ean,
#             preco_de,
#             preco_por
#         FROM `crawlers-fisia.silver.cadastro_admin_full`
#         WHERE sku_nike IN ({skus_formatados})
#         ORDER BY sku_nike
#     """

#     produtos = client.query(query)
#     df = produtos.to_dataframe()

#     if df.empty:
#         raise ValueError(f"⚠️ Nenhum produto encontrado para SKUs: {sku}")

#     df["ean"] = df["ean"].astype(str).str.split('.').str[0]
#     df["preco_de"] = df["preco_de"].apply(lambda x: round(x, 2) if pd.notnull(x) else '')
#     df["preco_por"] = df["preco_por"].apply(lambda x: round(x, 2) if pd.notnull(x) else '')

#     # Campos desejados
#     df["cod_estilo"] = df["sku_nike"]
#     df["product_name"] = df["nome_do_produto"]
#     df["pricetable_0_code"] = canal
#     df["pricetable_0_action ( decrease, increase ou  overwrite)"] = "overwrite"

#     # Colunas que devem ser mantidas
#     df["pricetable_0_percentage"] = ''
#     df["pricetable_1_code"] = ''
#     df["pricetable_1_action  ( decrease, increase ou  overwrite)"] = ''
#     df["pricetable_1_price"] = ''
#     df["pricetable_1_special_price"] = ''
#     df["pricetable_1_percentage"] = ''
#     df["pricetable_2_code"] = ''
#     df["pricetable_2_action"] = ''
#     df["pricetable_2_price"] = ''
#     df["pricetable_2_special_price"] = ''
#     df["pricetable_2_percentage"] = ''

#     # Colunas finais para o Excel (sem pricetable_0_price e pricetable_0_special_price)
#     df_final = df[[
#         "ean", "preco_de", "preco_por", "cod_estilo",
#         "pricetable_0_code", "pricetable_0_action ( decrease, increase ou  overwrite)",
#         "product_name", "pricetable_0_percentage",
#         "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
#         "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
#         "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
#         "pricetable_2_special_price", "pricetable_2_percentage"
#     ]].rename(columns={
#         "ean": "sku",
#         "preco_de": "price",
#         "preco_por": "special_price"
#     })

#     output_path = f"relatorio_produtos_{canal}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
#     df_final.to_excel(output_path, index=False)
#     return output_path

from google.cloud import bigquery
import pandas as pd
from datetime import datetime

def gerar_excel_precos(skus: list, canal: str):
    client = bigquery.Client()

    if not skus:
        raise ValueError("Nenhum SKU foi fornecido.")

    skus_formatados = ",".join([f"'{s}'" for s in skus])

    filtro_canal = f"AND price_table_label = '{canal}'" if canal else ""

    query = f"""
        SELECT 
            sku AS cod_estilo,
            name AS product_name,
            ean,
            price AS price,
            special_price AS special_price,
            price_table_label AS pricetable_0_code,
            price_table_price AS pricetable_0_price,
            price_table_special_price AS pricetable_0_special_price
        FROM `crawlers-fisia.landing.produtos_pluggto`
        WHERE sku IN ({skus_formatados})
        {filtro_canal}
        ORDER BY sku
    """

    produtos = client.query(query)
    df = produtos.to_dataframe()

    if df.empty:
        raise ValueError(f"⚠️ Nenhum produto encontrado para SKUs: {skus}")

    # Tratamento de campos
    df["pricetable_0_action ( decrease, increase ou  overwrite)"] = "overwrite"
    df["pricetable_0_percentage"] = ''
    df["pricetable_1_code"] = ''
    df["pricetable_1_action  ( decrease, increase ou  overwrite)"] = ''
    df["pricetable_1_price"] = ''
    df["pricetable_1_special_price"] = ''
    df["pricetable_1_percentage"] = ''
    df["pricetable_2_code"] = ''
    df["pricetable_2_action"] = ''
    df["pricetable_2_price"] = ''
    df["pricetable_2_special_price"] = ''
    df["pricetable_2_percentage"] = ''

    # Ajuste de tipos numéricos
    df["price"] = pd.to_numeric(df["price"], errors="coerce").round(2)
    df["special_price"] = pd.to_numeric(df["special_price"], errors="coerce").round(2)
    df["pricetable_0_price"] = pd.to_numeric(df["pricetable_0_price"], errors="coerce").round(2)
    df["pricetable_0_special_price"] = pd.to_numeric(df["pricetable_0_special_price"], errors="coerce").round(2)

    # Reordenação e renomeação final
    df_final = df[[
        "cod_estilo", "product_name", "ean", "price", "special_price",
        "pricetable_0_code", "pricetable_0_action ( decrease, increase ou  overwrite)",
        "pricetable_0_price", "pricetable_0_special_price", "pricetable_0_percentage",
        "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
        "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
        "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
        "pricetable_2_special_price", "pricetable_2_percentage"
    ]].rename(columns={
        "ean": "sku"
    })

    output_path = f"relatorio_produtos_{canal or 'todos'}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
    df_final.to_excel(output_path, index=False)
    return output_path

