import pandas as pd
from urllib.parse import urlparse

# Load the dataset
file_path = "/home/abhidha/Downloads/DataHut_AT_Billa_PriceExtractions_20251015.CSV"
df = pd.read_csv(file_path, delimiter='|')



# displaying row numbers having empty regular price

# Find rows where 'regular_price' is empty or blank
empty_rows = df[df["regular_price"].isna() | (df["regular_price"].astype(str).str.strip() == "")]

if empty_rows.empty:
    print("✅ No empty 'regular_price' rows found.")
else:
    print("⚠️ Empty 'regular_price' found in rows:")
    for _, row in empty_rows.iterrows():
        print(f"Unique ID: {row.get('unique_id', 'N/A')}")

# -- print total count ---
print(f"\nTotal empty rows: {len(empty_rows)}")





# --- Define columns to check ---
price_columns = ["regular_price", "selling_price", "promotion_price", "grammage_quantity"]

# --- Sets to store row indices with issues ---
comma_rows = set()
multiple_dots_rows = set()
letter_rows = set()

# --- Loop through each price column ---
for col in price_columns:
    # Work only on non-null values
    df_non_null = df[df[col].notna()].copy()
    df_non_null[col] = df_non_null[col].astype(str).str.strip()

    # --- Rows with commas ---
    comma_indices = df_non_null[df_non_null[col].str.contains(",", na=False)].index
    comma_rows.update(comma_indices)

    # --- Rows with multiple dots ---
    multiple_dot_indices = df_non_null[df_non_null[col].str.count(r"\.") > 1].index
    multiple_dots_rows.update(multiple_dot_indices)

    # --- Rows with letters ---
    letter_indices = df_non_null[
        (df_non_null[col] != "") &
        df_non_null[col].str.contains(r"[A-Za-z]", na=False)
    ].index
    letter_rows.update(letter_indices)

# --- Print results (row numbers only) ---
if comma_rows:
    print("\n=== Rows with Commas in Price Columns ===")
    print(sorted([i + 2 for i in comma_rows]))  # +2 for header offset
else:
    print("\n✅ No rows with commas found in price columns.")

if multiple_dots_rows:
    print("\n=== Rows with Multiple Dots in Price Columns ===")
    print(sorted([i + 2 for i in multiple_dots_rows]))
else:
    print("\n✅ No rows with multiple dots found in price columns.")

if letter_rows:
    print("\n=== Rows with Letters in Price Columns ===")
    print(sorted([i + 2 for i in letter_rows]))
else:
    print("\n✅ No rows with letters found in price columns.")



# Check if 'percentage_discount' column exists
if 'percentage_discount' in df.columns:
    # Filter rows containing '%'
    percentage_symbol_rows = df[
        df['percentage_discount'].astype(str).str.contains('%', na=False)
    ]

    # Print results
    if not percentage_symbol_rows.empty:
        print("\n⚠️ Percentage Symbol Issue Found:")
        print(f"Found {len(percentage_symbol_rows)} rows containing '%' in 'percentage_discount'.\n")
        for _, row in percentage_symbol_rows.iterrows():
            print(f"Unique ID: {row.get('unique_id', 'N/A')} | percentage_discount: {row['percentage_discount']}")
    else:
        print("\n✅ The 'percentage_discount' column is free from '%' symbols.")
else:
    print("\n❌ 'percentage_discount' column not found in the dataset.")





# --- Define valid UOM mapping (exact matches only) ---
uom_map = {
    "btl": ["Teebeutel Packung", "Teebeutel", "Beutel", "Btl",
            "Teebeutel Karton", "Teebeutel Paket", "Packung Beutel"],
    "stuck": ["Portion Packung", "ANW"],
    "wg": ["wg", "Waschgänge", "Waschgang"]
}

# --- Normalize columns ---
# Ensure site_shown_uom normalized (strip + lower)
df['site_uom_lower'] = df['site_shown_uom'].astype(str).str.strip().str.lower()

# Prepare expected column
df['expected_grammage_unit'] = pd.NA

# --- Assign expected grammage_unit only for exact matches ---
for category, valid_values in uom_map.items():
    valid_values_lower = [v.strip().lower() for v in valid_values]
    mask = df['site_uom_lower'].isin(valid_values_lower)
    df.loc[mask, 'expected_grammage_unit'] = category

# --- Normalize the actual grammage_unit for comparison ---
# convert NaN to empty string so comparison is consistent
df['grammage_unit_norm'] = df['grammage_unit'].fillna("").astype(str).str.strip().str.lower()

# --- Debug: how many rows had expected assigned ---
assigned_count = df['expected_grammage_unit'].notna().sum()
print(f"Rows with expected_grammage_unit assigned: {assigned_count}")

# --- Identify mismatches ---
mismatch_mask = (
    df['expected_grammage_unit'].notna() &
    (df['grammage_unit_norm'] != df['expected_grammage_unit'])
)

mismatches = df.loc[mismatch_mask, ['unique_id', 'site_shown_uom', 'grammage_unit', 'expected_grammage_unit', 'grammage_unit_norm']]

# --- Print mismatches (no Excel export) ---
if not mismatches.empty:
    print("\n⚠️ Mismatched 'grammage_unit' detected (showing unique_id and site_shown_uom):")
    for _, row in mismatches.iterrows():
        print(f"Unique ID: {row['unique_id']} | site_shown_uom: {row['site_shown_uom']} | "
              f"grammage_unit (orig): {row['grammage_unit']} | grammage_unit_norm: {row['grammage_unit_norm']} | "
              f"expected: {row['expected_grammage_unit']}")
    print(f"\nTotal mismatched rows: {len(mismatches)}")
else:
    print("✅ No grammage_unit mismatches detected.")


# multiple dot in price per unit

# --- Check if column exists ---
if "price_per_unit" in df.columns:
    # Convert to string and clean spaces, handle NaN
    df["price_per_unit"] = df["price_per_unit"].fillna("").astype(str).str.strip()

    # Create a cleaned version where 'Abtr.G' (case-insensitive) is normalized to 'abtrg'
    # so the dot in 'Abtr.G' won't be counted.
    df["ppu_clean_abtrg"] = df["price_per_unit"].str.replace(r"(?i)abtr\.g", "abtrg", regex=True)

    # Count dots on the cleaned value
    df["dot_count_clean"] = df["ppu_clean_abtrg"].str.count(r"\.")

    # Rows with more than one dot in the cleaned string are errors
    multiple_dots_mask = df["dot_count_clean"] > 1
    multiple_dots_price = df.loc[multiple_dots_mask]

    # --- Print results ---
    if not multiple_dots_price.empty:
        print(f"\n⚠️ Found {len(multiple_dots_price)} rows with multiple dots in 'price_per_unit' (after ignoring Abtr.G):")
        for idx, row in multiple_dots_price.iterrows():
            # Excel-style row number = index + 2 (header row = 1)
            print(f"Row: {idx + 2} | Unique ID: {row.get('unique_id', 'N/A')} | price_per_unit: {row['price_per_unit']} | dots: {int(row['dot_count_clean'])}")
    else:
        print("\n✅ No rows with multiple dots found in 'price_per_unit' (after ignoring Abtr.G).")
else:
    print("\n❌ 'price_per_unit' column not found in the dataset.")



## issues in grammage_quanity


col = "grammage_quantity"

if col in df.columns:
    # Convert to string to safely apply regex
    df[col] = df[col].astype(str)

    # Find rows with space between numbers (e.g., "200 2", "1234 56")
    spaced_numbers = df[df[col].str.contains(r'\d+\s+\d+', na=False)]

    # Print results
    if not spaced_numbers.empty:
        print(f"\n⚠️ Found {len(spaced_numbers)} rows with spaces between numbers in '{col}':\n")
        for idx, row in spaced_numbers.iterrows():
            print(f"Unique ID: {row.get('unique_id', 'N/A')} | {col}: {row[col]}")
    else:
        print(f"\n✅ No rows with spaces between numbers found in '{col}'.")
else:
    print(f"\n❌ '{col}' column not found in the dataset.")



#checking slovenia conditions 

# Ensure promotion_description is clean
df["promotion_description"] = df["promotion_description"].astype(str).str.lower().str.strip()

# Keywords to check
keywords = ["trajno znižano", "znižano"]

# Filter rows where promotion_description contains either keyword
znižano_rows = df[df["promotion_description"].str.contains("|".join(keywords), na=False)]

# From those, find rows where promotion_price is NOT empty
invalid_rows = znižano_rows[
    znižano_rows["promotion_price"].notna() &
    (znižano_rows["promotion_price"].astype(str).str.strip() != "")
]

# Print invalid rows
if not invalid_rows.empty:
    print("\n⚠️ Promotion Price Issue Found:")
    print(f"{len(invalid_rows)} rows where 'promotion_description' is 'Trajno znižano' or 'znižano' but 'promotion_price' is not empty.\n")
    for idx, row in invalid_rows.iterrows():
        print(f"Unique ID: {row.get('unique_id', 'N/A')} | promotion_description: {row['promotion_description']} | promotion_price: {row['promotion_price']}")
else:
    print("\n✅ All rows with 'Trajno znižano' or 'znižano' have empty 'promotion_price'. Data is consistent.")
