import pandas as pd
from urllib.parse import urlparse

# Load the dataset
file_path = "/home/abhidha/Downloads/DataHut_AT_Interspar_PriceExtractions_20250725.CSV"
                                   

df = pd.read_csv(file_path, delimiter='|')


# Total columns

columns = [col for col in df.columns]
print(columns)
print(f"Total number of columns: {len(columns)}")


#  Empty columns
empty_columns = [col for col in df.columns if df[col].isnull().all()]
print("Empty Columns ")
print(empty_columns if empty_columns else "No completely empty columns found.")

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
    print(f"site_shown_uom:", df['site_shown_uom'].notnull().sum())
    print(f"competitor_name:", df['competitor_name'].notnull().sum())
    print(f"extraction_date:", df['extraction_date'].notnull().sum())
    print(f"currency:", df['currency'].notnull().sum())

    
    
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

#  Unique values in specific columns
specific_columns = ["competitor_name", "extraction_date", "grammage_unit", "currency"]
print("\n Unique Values in Specific Columns \n")
for column in specific_columns:
    if column in df.columns:
        unique_values = df[column].dropna().unique()
        print(f"{column} ({len(unique_values)} unique values):")
        print(unique_values, "\n")
    else:
        print(f"{column} column not found in the dataset.\n")

# Define price columns
price_columns = ["regular_price", "selling_price", "promotion_price","price_per_unit","grammage_quantity"] 

# DataFrame to store rows with issues
comma_prices = pd.DataFrame()
multiple_dots_prices = pd.DataFrame()

# Check for commas and multiple dots in price columns
for col in price_columns:
    df[col] = df[col].astype(str)  # Convert to string to avoid errors

    # Filter rows containing commas
    comma_filtered_rows = df[df[col].str.contains(',', na=False)]
    comma_prices = pd.concat([comma_prices, comma_filtered_rows])

    # Filter rows containing more than one dot
    multiple_dots_filtered_rows = df[df[col].str.count(r'\.') > 1]
    multiple_dots_prices = pd.concat([multiple_dots_prices, multiple_dots_filtered_rows])

# Save rows with commas in price columns to an Excel file
if not comma_prices.empty:
    print("\n=== Comma Issue in Price Columns ===")
    print("Rows with commas in price columns found.")
    comma_prices.to_excel("comma_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'comma_price_rows.xlsx'.")
else:
    print("\nNo rows with commas found in the price columns.")

# Save rows with multiple dots in price columns to an Excel file
if not multiple_dots_prices.empty:
    print("\n=== Multiple Dots Issue in Price Columns ===")
    print("Rows with multiple dots in price columns found.")
    multiple_dots_prices.to_excel("multiple_dots_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'multiple_dots_price_rows.xlsx'.")
else:
    print("\nNo rows with multiple dots found in the price columns.")
#  Check if 'percentage_discount' column contains '%' symbol
if 'percentage_discount' in df.columns:
    percentage_symbol_rows = df[df['percentage_discount'].astype(str).str.contains('%','-', na=False)]
    
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


# Define your site‑shown uom categories
uom_map = {
    "btl": ["Teebeutel Packung", "Teebeutel", "Beutel", "Btl", 
            "Teebeutel Karton", "Teebeutel Paket", "Packung Beutel"],
    "stuck": ["Portion Packung", "ANW"],
    "wg": ["wg", "Waschgänge"]
}

# Flatten lookup for quick detection
lookup = {(unit.lower(), category): category 
          for category, units in uom_map.items() 
          for unit in units}

# Create normalized lower-case column for matching
df['site_uom_lower'] = df['site_shown_uom'].astype(str).str.lower()

# Create expected grammage_unit based on site_shown_uom
df['expected_grammage_unit'] = None

for category, units in uom_map.items():
    mask = df['site_uom_lower'].str.contains(
        '|'.join([u.lower() for u in units]), na=False
    )
    df.loc[mask, 'expected_grammage_unit'] = category

# Identify mismatches: when expected exists and df['grammage_unit'] is different
mismatch_mask = df['expected_grammage_unit'].notna() & (
    df['grammage_unit'].astype(str).str.lower() != df['expected_grammage_unit']
)

mismatches = df.loc[mismatch_mask, [
    'unique_id', 'site_shown_uom', 'grammage_unit', 'expected_grammage_unit'
]]

if not mismatches.empty:
    mismatches.to_excel("grammage_uom_mismatches.xlsx", index=False, engine='openpyxl')
    print(f"Found {len(mismatches)} rows where grammage_unit differs from expectation.")
else:
    print("No grammage_unit mismatches detected.")

# Optionally, if you want to *enforce* grammage_unit:
df['grammage_unit'] = df.apply(
    lambda row: row['expected_grammage_unit']
                if pd.notna(row['expected_grammage_unit'])
                else row['grammage_unit'],
    axis=1
)
