import os
import pandas as pd
import sweetviz as sv
import numpy as np

# Define file path
file_path = "/home/abhidha/Downloads/hw-training/2025-03-10/DataHut_AT_Dm_FullDump_20250327.CSV"

# Check file type
file_extension = os.path.splitext(file_path)[1].lower()

if file_extension == ".csv":
    # Try reading with ',' first, if it fails, use '|'
    try:
        df = pd.read_csv(file_path, delimiter=',')
    except pd.errors.ParserError:
        df = pd.read_csv(file_path, delimiter='|')

elif file_extension == ".json":
    try:
        df = pd.read_json(file_path, lines=True)  # Read JSON

        # 🔹 Replace None and empty strings with NaN
        df.replace({None: np.nan, "": np.nan}, inplace=True)

        # 🔹 Function to convert empty lists and dictionaries to NaN
        def replace_empty(x):
            if isinstance(x, list) and len(x) == 0:
                return np.nan
            if isinstance(x, dict) and len(x) == 0:
                return np.nan
            if isinstance(x, (list, dict)):
                return str(x)  # Convert lists/dicts to strings for compatibility
            return x

        # Apply function to each column
        df = df.applymap(replace_empty)

    except ValueError as e:
        print(f"Error reading JSON file: {e}")
        exit()

else:
    print("Unsupported file format.")
    exit()

# 🔹 **Find Completely Empty Columns**
empty_columns = df.columns[df.isnull().all()].tolist()  # Get columns where all values are NaN

# Save empty columns report
empty_columns_file = "empty_columns_report.csv"
pd.DataFrame(empty_columns, columns=["Empty Columns"]).to_csv(empty_columns_file, index=False)

print(f"Completely empty fields saved to: {empty_columns_file}")
print(f"Empty Columns: {empty_columns}")

df["grammage_quantity"] = df["grammage_quantity"].astype(str)


# 🔹 **Generate Sweetviz analysis report**
report = sv.analyze(df)

# Show the report
report.show_html("sweetviz_report.html")
report.show_notebook()
