import pandas as pd

# Read CSV file
df = pd.read_csv("/home/abhidha/Downloads/DataHut_AT_Fressnapf_FullDump_20250227.CSV", delimiter='|')

columns = [col for col in df.columns]
print(f"Total number of columns: {len(columns)}")

# Count total and unique URLs in 'pdp_url'
if 'pdp_url' in df.columns:
    total_urls = df['pdp_url'].notnull().sum()
    unique_urls = df['pdp_url'].nunique()
    total_id = df['unique_id'].notnull().sum()
    unique_id = df['unique_id'].nunique()
    print(f"\n=== URL Count ===")
    print(f"Total URLs: {total_urls}")
    print(f"Unique URLs: {unique_urls}")
    print(f"\n*** Unique_id Count ***")
    print(f"Total ID :", total_id)
    print(f"Unique ID :",unique_id)
    print(f"Breadcrumbs:", df['breadcrumb'].notnull().sum())
    



    #  Verify date format
date_columns = ['extraction_date', 'price_valid_from', 'promotion_valid_from', 'promotion_valid_upto']
date_format_issues = {}

for column in date_columns:
    if column in df.columns:
        try:
            pd.to_datetime(df[column], errors='raise')
        except Exception as e:
            date_format_issues[column] = str(e)

if date_format_issues:
    print("\nDate Format Issues ")
    for col, issue in date_format_issues.items():
        print(f"{col}: {issue}")
else:
    print("\nAll date columns are properly formatted.")

print("\n")


# List of columns to check
columns_to_check = ["unique_id", "competitor_name", "store_name", "store_addressline1", "store_addressline2",
                    "store_suburb", "store_state", "store_postcode", "store_addressid", "extraction_date",
                    "product_name", "brand", "brand_type", "grammage_quantity", "grammage_unit", "drained_weight",
                    "producthierarchy_level1", "producthierarchy_level2", "producthierarchy_level3",
                    "producthierarchy_level4", "producthierarchy_level5", "producthierarchy_level6",
                    "producthierarchy_level7", "regular_price", "selling_price", "price_was", "promotion_price",
                    "promotion_valid_from", "promotion_valid_upto", "promotion_type", "percentage_discount",
                    "promotion_description", "package_sizeof_sellingprice", "per_unit_sizedescription",
                    "price_valid_from", "price_per_unit", "multi_buy_item_count", "multi_buy_items_price_total",
                    "currency", "breadcrumb", "pdp_url", "variants", "product_description", "instructions",
                    "storage_instructions", "preparationinstructions", "instructionforuse", "country_of_origin",
                    "allergens", "age_of_the_product", "age_recommendations", "flavour", "nutritions",
                    "nutritional_information", "vitamins", "labelling", "grade", "region", "packaging", "receipies",
                    "processed_food", "barcode", "frozen", "chilled", "organictype", "cooking_part", "handmade",
                    "max_heating_temperature", "special_information", "label_information", "dimensions",
                    "special_nutrition_purpose", "feeding_recommendation", "warranty", "color", "model_number",
                    "material", "usp", "dosage_recommendation", "tasting_note", "food_preservation", "size",
                    "rating", "review", "file_name_1", "image_url_1", "file_name_2", "image_url_2", "file_name_3",
                    "image_url_3", "file_name_4", "image_url_4", "file_name_5", "image_url_5", "file_name_6",
                    "image_url_6", "competitor_product_key", "fit_guide", "occasion", "material_composition", "style",
                    "care_instructions", "heel_type", "heel_height", "upc", "features", "dietary_lifestyle",
                    "manufacturer_address", "importer_address", "distributor_address", "vinification_details",
                    "recycling_information", "return_address", "alchol_by_volume", "beer_deg", "netcontent",
                    "netweight", "site_shown_uom", "ingredients", "random_weight_flag", "instock", "promo_limit",
                    "product_unique_key", "multibuy_items_pricesingle", "perfect_match", "servings_per_pack",
                    "warning", "suitable_for", "standard_drinks", "environmental", "grape_variety", "retail_limit"]

# Columns expected to be empty
empty_expected = ["age_of_the_product","age_recommendations","alchol_by_volume","allergens","barcode","beer_deg","brand_type","care_instructions","chilled","competitor_product_key","cooking_part","country_of_origin","dietary_lifestyle","dimensions","dosage_recommendation","drained_weight","environmental","features","fit_guide","flavour","food_preservation","frozen","grade","grape_variety","handmade","heel_height","heel_type","importer_address","instructionforuse","instructions","label_information","labelling","manufacturer_address","material_composition","max_heating_temperature","model_number","multi_buy_item_count","multi_buy_items_price_total","multibuy_items_pricesingle","netweight","nutritional_information","nutritions","occasion","organictype","package_sizeof_sellingprice","packaging","per_unit_sizedescription","perfect_match","preparationinstructions","price_valid_from","processed_food","producthierarchy_level6","producthierarchy_level7","promo_limit","promotion_type","promotion_valid_from","promotion_valid_upto","random_weight_flag","receipies","recycling_information","region","return_address","servings_per_pack","special_information","standard_drinks","storage_instructions","store_addressid","store_addressline1","store_addressline2","store_name","store_postcode","store_state","store_suburb","style","suitable_for","tasting_note","upc","usp","vinification_details","vitamins","warranty"
]

# Find actual empty columns
empty_columns_actual = [col for col in columns_to_check if df[col].isnull().all() or (df[col] == '').all()]

# Columns expected to be empty but actually contain data
not_really_empty = [col for col in empty_expected if col not in empty_columns_actual]

# Columns that are empty but were **not** expected to be empty
unexpectedly_empty = [col for col in empty_columns_actual if col not in empty_expected]

# Print results
print("\nEmpty columns detected in dataset:", empty_columns_actual)

if not_really_empty:
    print("\nColumns expected to be empty but actually contain data:", not_really_empty)
else:
    print("\nAll expected empty columns are truly empty.")

if unexpectedly_empty:
    print("\nColumns that were NOT expected to be empty but are actually empty:", unexpectedly_empty)
else:
    print("\nNo unexpected empty columns found.")


#  Unique values in specific columns
specific_columns = ["competitor_name", "extraction_date", "grammage_unit", "currency","instock","organictype"]

print("\n Unique Values in Specific Columns \n")
for column in specific_columns:
    if column in df.columns:
        unique_values = df[column].dropna().unique()
        print(f"{column} ({len(unique_values)} unique values):")
        print(unique_values, "\n")
    else:
        print(f"{column} column not found in the dataset.\n")

#  Check for commas in price columns
price_columns = ["regular_price", "selling_price", "promotion_price"]
comma_prices = pd.DataFrame()

# Filter rows with commas in price columns
for col in price_columns:
    filtered_rows = df[df[col].astype(str).str.contains(',', na=False)]
    comma_prices = pd.concat([comma_prices, filtered_rows])

# Save rows with commas in price columns to an Excel file
if not comma_prices.empty:
    print("\n=== Comma Issue in Price Columns ===")
    print("Rows with commas in price columns found.")
    comma_prices.to_excel("comma_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'comma_price_rows.xlsx'.")
else:
    print("\nNo rows with commas found in the price columns.")


#  Check if 'percentage_discount' column contains '%' symbol
if 'percentage_discount' in df.columns:
    percentage_symbol_rows = df[df['percentage_discount'].astype(str).str.contains('%', na=False)]
    
    if not percentage_symbol_rows.empty:
        print("\n=== Percentage Symbol Issue ===")
        count_percentage_rows = len(percentage_symbol_rows)
        print(f"Found {count_percentage_rows} rows containing '%' in 'percentage_discount'.")
        percentage_symbol_rows.to_excel("percentage_symbol_issues.xlsx", index=False, engine='openpyxl')
        print("Filtered rows saved to 'percentage_symbol_issues.xlsx'.")
    else:
        print("\nThe 'percentage_discount' column is free from '%' symbols.")
else:
    print("\n'percentage_discount' column not found in the dataset.")
