import os
import pandas as pd
import sweetviz as sv

# Define file path
file_path = "/home/abhidha/Downloads/hw-training/2025-03-11/dari_ae_2025_03_02.json"

# Check file type
file_extension = os.path.splitext(file_path)[1].lower()

# Function to load different file types dynamically
def load_data(file_path, file_extension):
    try:
        if file_extension == ".csv":
            # Try reading with ',' first, if it fails, use '|'
            try:
                df = pd.read_csv(file_path, delimiter=',')
            except pd.errors.ParserError:
                df = pd.read_csv(file_path, delimiter='|')

        elif file_extension == ".json":
            df = pd.read_json(file_path, lines=True)  # Enables reading multi-line JSON

            # Check for dictionary or list-like columns
            complex_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, (dict, list))).any()]
            if complex_columns:
                print(f"Columns containing dictionaries/lists: {complex_columns}")
                # Convert lists/dictionaries to strings for compatibility
                df[complex_columns] = df[complex_columns].astype(str)

        elif file_extension == ".xlsx" or file_extension == ".xls":
            df = pd.read_excel(file_path)

        else:
            print(f"Unsupported file format: {file_extension}")
            exit()

        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        exit()

# Load the data based on file extension
df = load_data(file_path, file_extension)

# 🔹 **Find Completely Empty Columns**
empty_columns = df.columns[df.isnull().all()].tolist() 

# Save empty columns report
empty_columns_file = "empty_columns_report.csv"
pd.DataFrame(empty_columns, columns=["Empty Columns"]).to_csv(empty_columns_file, index=False)

print(f"Completely empty fields saved to: {empty_columns_file}")
print(f"Empty Columns: {empty_columns}")

# 🔹 **Check for Duplicate Rows**
duplicate_rows = df[df.duplicated()]
duplicate_rows_file = "duplicate_rows_report.csv"
duplicate_rows.to_csv(duplicate_rows_file, index=False)

print(f"Duplicate rows saved to: {duplicate_rows_file}")
print(f"Number of duplicate rows: {len(duplicate_rows)}")

# 🔹 **Check for Data Types Consistency**
data_types = df.dtypes
print(f"Data Types:\n{data_types}")

# 🔹 **Generate Sweetviz Analysis Report**
report = sv.analyze(df)

# Show the report
report.show_html("sweetviz_report.html")
report.show_notebook()
