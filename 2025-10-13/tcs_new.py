import pandas as pd
from urllib.parse import urlparse

# Load the dataset
file_path = "/home/abhidha/Downloads/DataHut_AT_Billa_PriceExtractions_20251017.CSV"
df = pd.read_csv(file_path, delimiter='|')

# Total columns
columns = [col for col in df.columns]
print(columns)
print(f"Total number of columns: {len(columns)}")

# Empty columns
empty_columns = [col for col in df.columns if df[col].isnull().all()]
print("Empty Columns")
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
    print(f"Total ID: {total_id}")
    print(f"Unique ID: {unique_id}")
    print(f"Breadcrumbs: {df['breadcrumb'].notnull().sum()}")
    print(f"site_shown_uom: {df['site_shown_uom'].notnull().sum()}")
    print(f"competitor_name: {df['competitor_name'].notnull().sum()}")
    print(f"extraction_date: {df['extraction_date'].notnull().sum()}")
    print(f"currency: {df['currency'].notnull().sum()}")

# Verify date format
date_columns = ['extraction_date', 'price_valid_from', 'promotion_valid_from', 'promotion_valid_upto']
date_format_issues = {}

for column in date_columns:
    if column in df.columns:
        try:
            pd.to_datetime(df[column], errors='raise')
        except Exception as e:
            date_format_issues[column] = str(e)

if date_format_issues:
    print("\nDate Format Issues")
    for col, issue in date_format_issues.items():
        print(f"{col}: {issue}")
else:
    print("\nAll date columns are properly formatted.")

# Unique values in specific columns
specific_columns = ["competitor_name", "extraction_date", "grammage_unit", "currency","instock","organictype"]
print("\n Unique Values in Specific Columns \n")
for column in specific_columns:
    if column in df.columns:
        unique_values = df[column].dropna().unique()
        print(f"{column} ({len(unique_values)} unique values):")
        print(unique_values, "\n")
    else:
        print(f"{column} column not found in the dataset.\n")








# Select required columns and check for empty regular prices
required_columns = ["unique_id", "pdp_url", "regular_price", "selling_price", "product_name","promotion_description"]
df_selected = df[required_columns]

empty_price_df = df_selected[
    df_selected["regular_price"].isna() |
    (df_selected["regular_price"].astype(str).str.strip() == "")
]
empty_price_df.to_excel("empty_regular_price.xlsx", index=False)
print("Excel file created: empty_regular_price.xlsx")

# Define price columns
price_columns = ["regular_price", "selling_price", "promotion_price", "grammage_quantity"]




# DataFrames to store rows with issues
comma_prices = pd.DataFrame()
multiple_dots_prices = pd.DataFrame()
letter_prices = pd.DataFrame()
seen_letter_indices = set()

for col in price_columns:
    # Work only on non-null values
    df_non_null = df[df[col].notna()].copy()
    df_non_null[col] = df_non_null[col].astype(str).str.strip()

    # Rows with commas
    comma_filtered = df_non_null[df_non_null[col].str.contains(",", na=False)]
    comma_prices = pd.concat([comma_prices, comma_filtered])

    # Rows with multiple dots
    multiple_dots_filtered = df_non_null[df_non_null[col].str.count(r"\.") > 1]
    multiple_dots_prices = pd.concat([multiple_dots_prices, multiple_dots_filtered])

    # Rows with letters (excluding blank and NaN)
    letter_filtered = df_non_null[
        (df_non_null[col] != "") &
        df_non_null[col].str.contains(r"[A-Za-z]", na=False)
    ]

    # Avoid duplicate rows
    new_indices = letter_filtered.index.difference(seen_letter_indices)
    if not new_indices.empty:
        letter_prices = pd.concat([letter_prices, letter_filtered.loc[new_indices]])
        seen_letter_indices.update(new_indices)

# Save issue files
if not comma_prices.empty:
    print("\n=== Comma Issue in Price Columns ===")
    print("Rows with commas in price columns found.")
    comma_prices.to_excel("comma_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'comma_price_rows.xlsx'.")
else:
    print("\nNo rows with commas found in the price columns.")

if not multiple_dots_prices.empty:
    print("\n=== Multiple Dots Issue in Price Columns ===")
    print("Rows with multiple dots in price columns found.")
    multiple_dots_prices.to_excel("multiple_dots_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'multiple_dots_price_rows.xlsx'.")
else:
    print("\nNo rows with multiple dots found in the price columns.")

if not letter_prices.empty:
    print("\n=== Letter Issue in Price Columns ===")
    print("Rows with letters in price columns found.")
    letter_prices.to_excel("letter_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'letter_price_rows.xlsx'.")
else:
    print("\nNo rows with letters found in the price columns.")


# Check if 'percentage_discount' column contains '%' symbol
if 'percentage_discount' in df.columns:
    percentage_symbol_rows = df[
        df['percentage_discount'].astype(str).str.contains('%', na=False)
    ]
    if not percentage_symbol_rows.empty:
        print("\n=== Percentage Symbol Issue ===")
        print(f"Found {len(percentage_symbol_rows)} rows containing '%' in 'percentage_discount'.")
        percentage_symbol_rows.to_excel("percentage_symbol_issues.xlsx", index=False, engine='openpyxl')
    else:
        print("\nThe 'percentage_discount' column is free from '%' symbols.\n")
else:
    print("\n'percentage_discount' column not found in the dataset.\n")

# Validate site_shown_uom vs grammage_unit
uom_map = {
    "btl": ["Teebeutel Packung", "Teebeutel", "Beutel", "Btl", 
            "Teebeutel Karton", "Teebeutel Paket", "Packung Beutel"],
    "stuck": ["Portion Packung", "ANW"],
    "wg": ["wg", "Waschgänge", "Waschgang"]
}

df['site_uom_lower'] = df['site_shown_uom'].astype(str).str.lower()
df['expected_grammage_unit'] = None

for category, units in uom_map.items():
    mask = df['site_uom_lower'].str.contains('|'.join([u.lower() for u in units]), na=False)
    df.loc[mask, 'expected_grammage_unit'] = category

mismatch_mask = df['expected_grammage_unit'].notna() & (
    df['grammage_unit'].astype(str).str.lower() != df['expected_grammage_unit']
)

mismatches = df.loc[mismatch_mask, [
    'unique_id', 'site_shown_uom', 'grammage_unit', 'expected_grammage_unit', 'pdp_url'
]]

if not mismatches.empty:
    mismatches.to_excel("grammage_uom_mismatches.xlsx", index=False, engine='openpyxl')
    print(f"Found {len(mismatches)} rows where grammage_unit differs from expectation.")
else:
    print("No grammage_unit mismatches detected.")

# Enforce grammage_unit from expected
df['grammage_unit'] = df.apply(
    lambda row: row['expected_grammage_unit']
    if pd.notna(row['expected_grammage_unit'])
    else row['grammage_unit'],
    axis=1
)

# multiple dot in price per unit

if "price_per_unit" in df.columns:
    # Convert to string
    df["price_per_unit"] = df["price_per_unit"].astype(str)

    # Filter rows with more than one dot in the value
    multiple_dots_price = df[df["price_per_unit"].str.count(r'\.') > 1]

    # Check and save
    if not multiple_dots_price.empty:
        print(f"\nFound {len(multiple_dots_price)} rows with multiple dots in 'price_per_unit'.")
        multiple_dots_price.to_excel("multiple_dots_price_per_unit.xlsx", index=False, engine='openpyxl')
        print("\nFiltered rows saved to 'multiple_dots_price_per_unit.xlsx'.")
    else:
        print("\nNo rows with multiple dots found in 'price_per_unit'.")
else:
    print("\n'price_per_unit' column not found in the dataset.")



col = "grammage_quantity"

if col in df.columns:
    # Convert to string to safely apply regex
    df[col] = df[col].astype(str)

    # Find rows with space between numbers 
    spaced_numbers = df[df[col].str.contains(r'\d+\s+\d+', na=False)]

    if not spaced_numbers.empty:
        print(f"\nFound {len(spaced_numbers)} rows with spaces between numbers in '{col}'.")
        spaced_numbers.to_excel("grammage_space_issues.xlsx", index=False, engine='openpyxl')
        print("\nFiltered rows saved to 'grammage_space_issues.xlsx'.")
    else:
        print(f"\nNo rows with spaces between numbers found in '{col}'.")
else:
    print(f"\n'{col}' column not found in the dataset.")



#checking slovenia conditions 

df["promotion_description"] = df["promotion_description"].astype(str).str.lower().str.strip()

# keywords to check
keywords = ["trajno znižano", "znižano"]

# Filter rows where promotion_description contains either keyword
znižano_rows = df[df["promotion_description"].str.contains("|".join(keywords), na=False)]

# From those, find rows where promotion_price is NOT empty
invalid_rows = znižano_rows[znižano_rows["promotion_price"].notna() & (znižano_rows["promotion_price"].astype(str).str.strip() != "")]

# Save invalid rows for review
if not invalid_rows.empty:
    print("\n=== Promotion Price Issue Found ===")
    print(f"{len(invalid_rows)} rows found where 'promotion_description' is 'Trajno znižano' or 'znižano' but 'promotion_price' is not empty.")
    invalid_rows.to_excel("invalid_promotion_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'invalid_promotion_price_rows.xlsx'.")
else:
    print("\n✅ All rows with 'Trajno znižano' or 'znižano' have empty 'promotion_price'. Data is consistent.")
