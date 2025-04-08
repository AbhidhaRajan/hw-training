import os
import pandas as pd
import sweetviz as sv
import numpy as np

# Get file path from user
file_path = input("Enter path to CSV or JSON file: ").strip()

if not os.path.exists(file_path):
    print("File not found.")
    exit()

ext = os.path.splitext(file_path)[1].lower()

# Load the data
if ext == '.csv':
    try:
        df = pd.read_csv(file_path, delimiter=',')
    except pd.errors.ParserError:
        df = pd.read_csv(file_path, delimiter='|')
elif ext == '.json':
    try:
        df = pd.read_json(file_path, lines=True)
        df.replace({None: np.nan, "": np.nan}, inplace=True)
        df = df.applymap(lambda x: np.nan if isinstance(x, (list, dict)) and not x else x)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        exit()
else:
    print("Unsupported file type.")
    exit()

# Start building the HTML report
html = """
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
<h1>QA Data Report – Unique Field Values</h1>
"""

for idx, col in enumerate(df.columns):
    unique_vals = df[col].dropna().unique()
    uid = f"field_{idx}"
    html += f"""
    <div class="field-block">
        <div class="field-header" onclick="toggle('{uid}')">{col}</div>
        <div class="unique-count">Unique values: {len(unique_vals)}</div>
        <ul class="unique-values" id="{uid}">
    """
    for val in unique_vals:
        html += f"<li>{val}</li>"
    html += "</ul></div>"

html += "</body></html>"

# Save the HTML report
output_file = "qa_field_uniques_report.html"
with open(output_file, "w") as f:
    f.write(html)

print(f"QA-style unique value report saved to: {output_file}")

# Optional: Generate Sweetviz report
sv_report = sv.analyze(df)
sv_report.show_html("sweetviz_report.html", open_browser=False)
print("Sweetviz report saved to: sweetviz_report.html")
