import pandas as pd
from urllib.parse import urlparse

# Load the dataset
file_path = "/home/abhidha/Downloads/mister_auto_2025_03_14.csv "
df = pd.read_csv(file_path, delimiter=',')

# Total columns

columns = [col for col in df.columns]
print(columns)
print(f"Total number of columns: {len(columns)}")

#  Empty columns
empty_columns = [col for col in df.columns if df[col].isnull().all()]
print("Empty Columns ")
print(empty_columns if empty_columns else "No completely empty columns found.")

print(f"Total number of empty columns: {len(empty_columns)}")
