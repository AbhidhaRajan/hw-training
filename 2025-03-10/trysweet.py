import os
import pandas as pd
import sweetviz as sv

# Define file path
file_path = "/home/abhidha/Downloads/DataHut_HU_Auchan_PriceExtractions_20250310.CSV"

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
        df = pd.read_json(file_path, lines=True)  # Enables reading multi-line JSON

        # Check for dictionary or list-like columns
        complex_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, (dict, list))).any()]

        if complex_columns:
            print(f"Columns containing dictionaries/lists: {complex_columns}")

            # Convert lists/dictionaries to strings for compatibility
            df[complex_columns] = df[complex_columns].astype(str)

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

# 🔹 **Generate Sweetviz analysis report**
report = sv.analyze(df)

# Show the report
report.show_html("sweetviz_report.html")
report.show_notebook()
