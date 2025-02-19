import pandas as pd


df = pd.read_csv("/home/abhidha/Downloads/DataHut_AT_Mueller_FullDump_20250220.CSV",delimiter='|')  

# List of columns to check
columns_to_check = [
"store_name","store_addressline1","store_addressline2","store_suburb","store_state",
"store_postcode","store_addressid","brand_type","drained_weight","promotion_valid_from","promotion_valid_upto",
"promotion_type","package_sizeof_sellingprice","per_unit_sizedescription","price_valid_from",
"multi_buy_item_count","multi_buy_items_price_total","preparationinstructions","age_of_the_product",
"nutritions","vitamins","labelling","grade","receipies","barcode","frozen","chilled","cooking_part",
"handmade","max_heating_temperature","label_information","dimensions","special_nutrition_purpose",
"warranty","usp","food_preservation","competitor_product_key","fit_guide","occasion","material_composition",
"style","heel_type","heel_height","upc","features","dietary_lifestyle","importer_address",
"distributor_address","vinification_details","recycling_information","return_address","beer_deg","netcontent",
"netweight","random_weight_flag","promo_limit",
"multibuy_items_pricesingle","perfect_match","servings_per_pack","standard_drinks","environmental","processed_food"

  ]


non_empty_columns = [col for col in columns_to_check if df[col].notna().any() and (df[col] != '').any()]


if non_empty_columns:
    print("Non-empty columns:", non_empty_columns)
else:
    print("All specified columns are empty.")