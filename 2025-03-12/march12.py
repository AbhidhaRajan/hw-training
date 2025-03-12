from pymongo import MongoClient
import pandas as pd
import sweetviz as sv
import os
from io import StringIO

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Adjust the URI as needed
db = client['MyTry']

# Function to check if a collection exists
def collection_exists(db, collection_name):
    return collection_name in db.list_collection_names()

# Function to load different file types dynamically
def load_data(content, extension):
    try:
        if extension == ".csv":
            # Convert the content to a pandas DataFrame
            try:
                df = pd.read_csv(StringIO(content), delimiter=',')
            except pd.errors.ParserError:
                df = pd.read_csv(StringIO(content), delimiter='|')

        elif extension == ".json":
            df = pd.read_json(StringIO(content), lines=True)  # Enables reading multi-line JSON

            # Check for dictionary or list-like columns
            complex_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, (dict, list))).any()]
            if complex_columns:
                print(f"Columns containing dictionaries/lists: {complex_columns}")
                # Convert lists/dictionaries to strings for compatibility
                df[complex_columns] = df[complex_columns].astype(str)

        else:
            print(f"Unsupported file format: {extension}")
            return None

        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Specify the collection name
collection_name = 'jsonn'

if collection_exists(db, collection_name):
    collection = db[collection_name]
    # Assuming each document in the collection represents a file with 'file_name' and 'file_content' fields
    for document in collection.find():
        file_name = document.get('file_name')
        file_content = document.get('file_content')  # This should be the actual data

        if file_name is None:
            print(f"Skipping document with missing 'file_name': {document}")
            continue

        file_extension = os.path.splitext(file_name)[1].lower()

        df = load_data(file_content, file_extension)

        if df is not None:
            # Find Completely Empty Columns
            empty_columns = df.columns[df.isnull().all()].tolist()

            # Save empty columns report
            empty_columns_file = f"empty_columns_report_{file_name}.csv"
            pd.DataFrame(empty_columns, columns=["Empty Columns"]).to_csv(empty_columns_file, index=False)

            print(f"Completely empty fields saved to: {empty_columns_file}")
            print(f"Empty Columns: {empty_columns}")

            # Check for Duplicate Rows
            duplicate_rows = df[df.duplicated()]
            duplicate_rows_file = f"duplicate_rows_report_{file_name}.csv"
            duplicate_rows.to_csv(duplicate_rows_file, index=False)

            print(f"Duplicate rows saved to: {duplicate_rows_file}")
            print(f"Number of duplicate rows: {len(duplicate_rows)}")

            # Data Types
            data_types = df.dtypes
            print(f"Data Types:\n{data_types}")

            # Sweetviz Analysis Report
            report = sv.analyze(df)

            # Show the report
            report_file = f"sweetviz_report_{file_name}.html"
            report.show_html(report_file)
            report.show_notebook()
        else:
            print(f"Failed to load data for file: {file_name}")
else:
    print(f"Collection '{collection_name}' does not exist in the database.")
