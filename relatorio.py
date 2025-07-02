# from google.cloud import bigquery
# import pandas as pd
# from datetime import datetime

# def gerar_excel_precos(skus: list, canal: str):
#     client = bigquery.Client()

#     if not skus:
#         raise ValueError("Nenhum SKU foi fornecido.")

#     skus_formatados = ",".join([f"'{s}'" for s in skus])

#     filtro_canal = f"AND price_table_label = '{canal}'" if canal else ""
#     incluir_ml_sku = canal == "MELI"

#     select_campos = """
#         sku AS cod_estilo,
#         name AS product_name,
#         ean,
#         price AS price,
#         special_price AS special_price,
#         price_table_label AS pricetable_0_code,
#         price_table_price AS pricetable_0_price,
#         price_table_special_price AS pricetable_0_special_price
#     """

#     if incluir_ml_sku:
#         select_campos += ", ML_sku"

#     query = f"""
#         SELECT 
#             {select_campos}
#         FROM `crawlers-fisia.landing.produtos_pluggto_bf`
#         WHERE sku IN ({skus_formatados})
#         {filtro_canal}
#         ORDER BY sku
#     """

#     produtos = client.query(query)
#     df = produtos.to_dataframe()

#     if df.empty:
#         raise ValueError(f"⚠️ Nenhum produto encontrado para SKUs: {skus}")

#     # Tratamento de campos
#     df["pricetable_0_action ( decrease, increase ou  overwrite)"] = "overwrite"
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

#     # Ajuste de tipos numéricos
#     for col in ["price", "special_price", "pricetable_0_price", "pricetable_0_special_price"]:
#         df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

#     # Reordenação e renomeação
#     colunas_base = [
#         "cod_estilo", "product_name", "ean", "price", "special_price",
#         "pricetable_0_code", "pricetable_0_action ( decrease, increase ou  overwrite)",
#         "pricetable_0_price", "pricetable_0_special_price", "pricetable_0_percentage",
#         "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
#         "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
#         "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
#         "pricetable_2_special_price", "pricetable_2_percentage"
#     ]

#         # Renomeia 'ean' para 'sku'
#     if "ean" in df.columns:
#         df = df.rename(columns={"ean": "sku"})

#     # Se canal for MELI, renomeia ML_sku → sku_parceiro
#     if incluir_ml_sku and "ML_sku" in df.columns:
#         df = df.rename(columns={"ML_sku": "sku_parceiro"})
#         colunas_base = [
#             "cod_estilo", "product_name", "sku_parceiro", "sku", "price", "special_price",
#             "pricetable_0_code", "pricetable_0_action ( decrease, increase ou  overwrite)",
#             "pricetable_0_price", "pricetable_0_special_price", "pricetable_0_percentage",
#             "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
#             "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
#             "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
#             "pricetable_2_special_price", "pricetable_2_percentage"
#         ]
#     else:
#         colunas_base = [
#             "cod_estilo", "product_name", "sku", "price", "special_price",
#             "pricetable_0_code", "pricetable_0_action ( decrease, increase ou  overwrite)",
#             "pricetable_0_price", "pricetable_0_special_price", "pricetable_0_percentage",
#             "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
#             "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
#             "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
#             "pricetable_2_special_price", "pricetable_2_percentage"
#         ]

#     df_final = df[colunas_base]

#     # Geração do arquivo Excel
#     output_path = f"relatorio_produtos_{canal or 'todos'}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
#     df_final.to_excel(output_path, index=False)

#     return output_path


from google.cloud import bigquery, storage
import pandas as pd
from datetime import datetime
from io import BytesIO

def upload_to_gcs(bucket_name, destination_blob_name, dataframe):
    """Faz upload do DataFrame como Excel diretamente para o GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Grava o Excel em memória
    excel_buffer = BytesIO()
    dataframe.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    # Upload direto do buffer
    blob.upload_from_file(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    print(f"✅ Arquivo salvo no GCS: gs://{bucket_name}/{destination_blob_name}")

    # Link para abrir no Console
    gcs_console_link = f"https://console.cloud.google.com/storage/browser/{bucket_name}/relatorios"

    return gcs_console_link

def gerar_excel_precos(skus: list, canal: str):
    client = bigquery.Client()

    if not skus:
        raise ValueError("Nenhum SKU foi fornecido.")

    skus_formatados = ",".join([f"'{s}'" for s in skus])

    filtro_canal = f"AND price_table_label = '{canal}'" if canal else ""
    incluir_ml_sku = canal == "MELI"

    select_campos = """
        sku AS cod_estilo,
        name AS product_name,
        ean,
        price AS price,
        special_price AS special_price,
        price_table_label AS pricetable_0_code,
        price_table_price AS pricetable_0_price,
        price_table_special_price AS pricetable_0_special_price
    """

    if incluir_ml_sku:
        select_campos += ", ML_sku"

    query = f"""
        SELECT 
            {select_campos}
        FROM `crawlers-fisia.landing.produtos_pluggto_bf`
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
    for col in ["price", "special_price", "pricetable_0_price", "pricetable_0_special_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

    # Reordenação e renomeação
    if "ean" in df.columns:
        df = df.rename(columns={"ean": "sku"})

    if incluir_ml_sku and "ML_sku" in df.columns:
        df = df.rename(columns={"ML_sku": "sku_parceiro"})
        colunas_base = [
            "cod_estilo", "product_name", "sku_parceiro", "sku", "price", "special_price",
            "pricetable_0_code", "pricetable_0_action ( decrease, increase ou  overwrite)",
            "pricetable_0_price", "pricetable_0_special_price", "pricetable_0_percentage",
            "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
            "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
            "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
            "pricetable_2_special_price", "pricetable_2_percentage"
        ]
    else:
        colunas_base = [
            "cod_estilo", "product_name", "sku", "price", "special_price",
            "pricetable_0_code", "pricetable_0_action ( decrease, increase ou  overwrite)",
            "pricetable_0_price", "pricetable_0_special_price", "pricetable_0_percentage",
            "pricetable_1_code", "pricetable_1_action  ( decrease, increase ou  overwrite)",
            "pricetable_1_price", "pricetable_1_special_price", "pricetable_1_percentage",
            "pricetable_2_code", "pricetable_2_action", "pricetable_2_price",
            "pricetable_2_special_price", "pricetable_2_percentage"
        ]

    df_final = df[colunas_base]

    # Geração do caminho no GCS
    bucket_name = "relatorio_produtos"  # <- Substitua pelo nome do seu bucket
    destination_blob_name = f"relatorios/relatorio_produtos_{canal or 'todos'}_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"

    gcs_uri = upload_to_gcs(bucket_name, destination_blob_name, df_final)

    
    return gcs_uri
