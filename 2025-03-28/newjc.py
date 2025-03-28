import os
import pandas as pd
import sweetviz as sv
import numpy as np

# Define file path
file_path = "/home/abhidha/Downloads/hw-training/2025-03-28/dubizzle_egp_2025_03_02.json"

# Check file type
file_extension = os.path.splitext(file_path)[1].lower()

if file_extension == ".csv":
    # Attempt to read the CSV file with ',' delimiter; if it fails, try '|'
    try:
        df = pd.read_csv(file_path, delimiter=',')
    except pd.errors.ParserError:
        df = pd.read_csv(file_path, delimiter='|')

    #  total number of columns
    total_columns = len(df.columns)
    print(f"Total number of columns: {total_columns}")

    
    if 'pdp_url' in df.columns:
        total_urls = df['pdp_url'].notnull().sum()
        unique_urls = df['pdp_url'].nunique()
        print(f"\n=== URL Count ===")
        print(f"Total URLs: {total_urls}")
        print(f"Unique URLs: {unique_urls}")

    
    if 'unique_id' in df.columns:
        total_ids = df['unique_id'].notnull().sum()
        unique_ids = df['unique_id'].nunique()
        print(f"\n=== Unique ID Count ===")
        print(f"Total IDs: {total_ids}")
        print(f"Unique IDs: {unique_ids}")

   
    if 'breadcrumb' in df.columns:
        breadcrumb_count = df['breadcrumb'].notnull().sum()
        print(f"\nBreadcrumbs count: {breadcrumb_count}")

    if 'site_shown_uom' in df.columns:
        site_shown_uom_count = df['site_shown_uom'].notnull().sum()
        print(f"Site Shown UOM count: {site_shown_uom_count}")

elif file_extension == ".json":
    try:
        df = pd.read_json(file_path, lines=True)  # Read JSON

        # Replace None and empty strings with NaN
        df.replace({None: np.nan, "": np.nan}, inplace=True)

        # Function to convert empty lists and dictionaries to NaN
        def replace_empty(x):
            if isinstance(x, list) and len(x) == 0:
                return np.nan
            if isinstance(x, dict) and len(x) == 0:
                return np.nan
            if isinstance(x, (list, dict)):
                return str(x)  
            return x

        # Apply function to each column
        df = df.applymap(replace_empty)

    except ValueError as e:
        print(f"Error reading JSON file: {e}")
        exit()

else:
    print("Unsupported file format.")
    exit()

# Find Completely Empty Columns
empty_columns = df.columns[df.isnull().all()].tolist()  
# Save empty columns report
empty_columns_file = "empty_columns_report_dubz.csv"
pd.DataFrame(empty_columns, columns=["Empty Columns"]).to_csv(empty_columns_file, index=False)

print(f"\nCompletely empty fields saved to: {empty_columns_file}")
print(f"Empty Columns: {empty_columns}")

# Convert 'grammage_quantity' column to string if it exists
if 'grammage_quantity' in df.columns:
    df["grammage_quantity"] = df["grammage_quantity"].astype(str)

# Generate Sweetviz analysis report
report = sv.analyze(df)

# Save and display the report
report.show_html("sweetviz_report_dubz.html", open_browser=False)
