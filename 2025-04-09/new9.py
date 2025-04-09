import os
import pandas as pd
import sweetviz as sv
import numpy as np

# Prompt user for file path
file_path = input("Enter the path to your data file: ").strip()

# Check if the file exists
if not os.path.exists(file_path):
    print("The file does not exist. Please check the path and try again.")
    exit()

# Determine file extension
file_extension = os.path.splitext(file_path)[1].lower()

# Initialize DataFrame
df = None

# Read the file based on its extension
if file_extension == ".csv":
    # Try reading with ',' delimiter; if it fails, try '|'
    try:
        df = pd.read_csv(file_path, delimiter=',')
    except pd.errors.ParserError:
        df = pd.read_csv(file_path, delimiter='|')
elif file_extension == ".json":
    try:
        df = pd.read_json(file_path, lines=True)
        # Replace None and empty strings with NaN
        df.replace({None: np.nan, "": np.nan}, inplace=True)
        # Function to convert empty lists and dictionaries to NaN
        def replace_empty(x):
            if isinstance(x, (list, dict)) and not x:
                return np.nan
            return x
        df = df.applymap(replace_empty)
    except ValueError as e:
        print(f"Error reading JSON file: {e}")
        exit()
else:
    print("Unsupported file format. Please provide a CSV or JSON file.")
    exit()

# Check if DataFrame is empty
if df.empty:
    print("The file is empty. Please provide a valid data file.")
    exit()

# Display total number of columns
total_columns = len(df.columns)
print(f"Total number of columns: {total_columns}")

# Identify the URL column (e.g., 'pdp_url')
url_column = 'pdp_url' if 'pdp_url' in df.columns else ('url' if 'url' in df.columns else None)


# Start building the HTML report
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>QA Unique Values Report</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }
        h1 { color: #333; }
        .field-block { margin-bottom: 20px; padding: 15px; border: 1px solid #ccc; background: #fff; border-radius: 8px; }
        .field-header { font-size: 18px; font-weight: bold; cursor: pointer; color: #007bff; }
        .unique-count { font-size: 14px; color: #555; }
        .unique-values { display: none; margin-top: 10px; font-size: 14px; color: #444; }
        .unique-values li { line-height: 1.5; }
    </style>
    <script>
        function toggle(id) {
            var elem = document.getElementById(id);
            elem.style.display = (elem.style.display === 'none') ? 'block' : 'none';
        }
    </script>
</head>
<body>
<h1>QA Data Report – Unique Field Values with URLs</h1>
"""

# Iterate through each column to process unique values
for idx, col in enumerate(df.columns):
    unique_vals = df[col].dropna().unique()
    uid = f"field_{idx}"
    html_content += f"""
    <div class="field-block">
        <div class="field-header" onclick="toggle('{uid}')">{col}</div>
        <div class="unique-count">Unique values: {len(unique_vals)}</div>
        <ul class="unique-values" id="{uid}">
    """
    # For each unique value, find the corresponding URL(s)
    for val in unique_vals:
        # Find the first occurrence of the unique value
        row = df[df[col] == val].iloc[0]
        url = row[url_column] if url_column and pd.notna(row[url_column]) else '#'
        html_content += f'<li>{val} - <a href="{url}" target="_blank">Link</a></li>'
    html_content += "</ul></div>"

html_content += "</body></html>"

# Save the HTML report
report_file = "qa_unique_values_with_urls_report.html"
with open(report_file, "w") as file:
    file.write(html_content)

print(f"\nQA unique values report with URLs saved to: {report_file}")

# Generate Sweetviz analysis report
report = sv.analyze(df)
sweetviz_report_file = "sweetviz_report.html"
report.show_html(sweetviz_report_file, open_browser=False)
print(f"Sweetviz report saved to: {sweetviz_report_file}")
