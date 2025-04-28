def parse_skus(skus_input:str):
    try:
        if "," in skus_input:
            skus_list = [sku.strip() for sku in skus_input.split(",")]
        else:
            skus_list = skus_input.split()
    except:
        skus_list = None
    return skus_list
