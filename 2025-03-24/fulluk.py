import pandas as pd

# Read CSV file
df = pd.read_csv("/home/abhidha/Downloads/DataHut_UK_Next_FullDump_20250325.CSV", delimiter='|')

columns = [col for col in df.columns]
print(f"Total number of columns: {len(columns)}")


columns_actual= ["dh_unique_id","dh_unique_id_b64","unique_id","competitor_name","extraction_date",
"product_name","brand","producthierarchy_level1","producthierarchy_level2",
"producthierarchy_level3","producthierarchy_level4","producthierarchy_level5",
"regular_price","selling_price","promotion_price","promotion_valid_from",
"promotion_valid_upto","promotion_type","promotion_description","currency",
"breadcrumb","pdp_url","variant_size","product_description","country_of_origin",
"instructions","color","model_number","material","size","rating","review",
"file_name_1","image_url_1","file_name_2","image_url_2","file_name_3",
"image_url_3","competitor_product_key","fit_guide","occasion",
"material_composition","style","care_instructions","upc","features","gender",
"clothing_type","clothing_fit","clothing_length","collar_type","pattern",
"pocket","fastener_closure_type","rise_pants_capris","pant_leg_cut","iron",
"stretch","maternity","thermal","clothing_weight","upper_body_strap_configuration",
"clothing_leg_bottom_opening_style","cuffs_style","neck_style","clothing_length_style",
"sleeve_length_style","ean","body_fit","variant_color","social_proof_label",
"stock_availability","others"]


# Check for missing and extra columns
missing_columns = [col for col in columns_actual if col not in columns]
extra_columns = [col for col in columns if col not in columns_actual]

if missing_columns:
    print("\n⚠️ Missing columns in dataset:", missing_columns)
else:
    print("\n✅ No missing columns.")

if extra_columns:
    print("\n⚠️ Extra columns found in dataset:", extra_columns)
else:
    print("\n✅ No extra columns.")










# List of columns to check
columns_to_check = columns

# Assuming quoted_data is a comma-separated string of column names
empty_expected = ["producthierarchy_level4","producthierarchy_level5","promotion_price","promotion_valid_from",
"promotion_valid_upto","promotion_type","country_of_origin","instructions","model_number",
"material","competitor_product_key","fitguide","occasion","upc","features","clothing_type",
"clothing_Length","collar_type","pattern","Pockets","fastener_Closure_type","rise",
"pant_leg_cut","iron","stretch","maternity","thermal","clothing_weight",
"upper_body_strap_configuration","clothing_leg_bottom_opening_style","cuffs_style",
"neck_style","clothing_length_style","sleeve_length_style","ean","body_fit",
"file_name_2","image_url_2","file_name_3","image_url_3","promotion_description"]

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




