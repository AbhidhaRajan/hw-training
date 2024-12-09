import streamlit as st
import json
import pandas as pd
import re

# Predefined set of correct fields
VALID_FIELDS = set([
    "first_name", "middle_name", "last_name", "office_name", "title",
    "description", "languages", "image_url", "address", "city", "state",
    "country", "zipcode", "office_phone_numbers", "agent_phone_numbers",
    "email", "website", "social", "profile_url"
])

# Function to parse and load JSON data
def load_json_data(file):
    content = file.read().decode("utf-8")
    return json.loads(content)



def validate_numbers(df, column_name):
    # Regular expression to match valid phone numbers
    phone_pattern = re.compile(r'^\+?[0-9\s\-\(\)\[\]]{7,20}$')
    # Find rows with invalid phone numbers
    invalid_entries = df[~df[column_name].str.match(phone_pattern, na=False)]
    return invalid_entries



# Function to validate email addresses
def validate_email_format(df, column_name):
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    invalid_emails = df[~df[column_name].str.match(email_regex, na=False)]
    return invalid_emails

# Function to validate URL formats
def check_url_format(df, column_name):
    url_regex = re.compile(r"^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(/[a-zA-Z0-9-_.?=&%]*)?$")
    invalid_urls = df[~df[column_name].str.match(url_regex, na=False)]
    return invalid_urls

# Function to detect columns with missing values
def find_missing_data(df):
    return df.columns[df.isnull().all()].tolist()

# Function to ensure the correct column names
def verify_column_names(data):
    incorrect_columns = [col for col in data.keys() if col not in VALID_FIELDS]
    return incorrect_columns

# Function to check field name format
def validate_column_name_format(data):
    improperly_named = [field for field in data.keys() if not field.islower() or "_" not in field]
    return improperly_named

# Function to identify missing mandatory fields
def check_required_fields(df, required_fields):
    absent_fields = [field for field in required_fields if field not in df.columns or df[field].isnull().all()]
    return absent_fields

# Function to expand 'social' column into individual columns
def expand_social_links(df):
    if 'social' in df.columns:
        social_expanded = df['social'].apply(pd.Series)
        return pd.concat([df, social_expanded], axis=1)
    return df

# Function to validate social media links
def verify_social_links(df, column_name):
    social_regex = {
        "facebook": r"^(https?://)?(www\.)?facebook\.com/[a-zA-Z0-9_.]+$",
        "twitter": r"^(https?://)?(www\.)?twitter\.com/[a-zA-Z0-9_]+$",
        "linkedin": r"^(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+$"
    }
    invalid_socials = []
    for idx, url in enumerate(df[column_name]):
        if not any(re.match(pattern, str(url)) for pattern in social_regex.values()):
            invalid_socials.append((idx, url))
    return invalid_socials

# Function to validate file naming convention
def validate_file_name(name):
    return bool(re.match(r'^[a-zA-Z0-9_]+_\d{4}_\d{2}_\d{05}\.json$', name))

def main():
    st.title("My JSON QA Application")
    uploaded_file = st.file_uploader("Upload JSON File", type="json")

    if uploaded_file:
        try:
            json_data = load_json_data(uploaded_file)
            df = pd.DataFrame(json_data)

            st.write("**Uploaded File Information**")
            st.write(f"File Name: {uploaded_file.name}")
            
            if validate_file_name(uploaded_file.name):
                st.success("File name format is valid.")
            else:
                st.error("Invalid file name format. Expected: filename_YYYY_MM_DD.json")

            st.write(f"Number of Rows: {len(df)}")
            df = expand_social_links(df)

            st.write("**Check Required Fields**")
            required_fields = st.multiselect("Select Required Fields", options=df.columns.tolist(), default=[])
            missing_fields = check_required_fields(df, required_fields)
            if missing_fields:
                st.error(f"Missing Required Fields: {', '.join(missing_fields)}")
            else:
                st.success("All required fields are present.")

            st.write("**Field Name Verification**")
            invalid_columns = verify_column_names(json_data[0])
            if invalid_columns:
                st.error(f"Incorrect Column Names: {', '.join(invalid_columns)}")
            else:
                st.success("All column names are valid.")

            field_name_errors = validate_column_name_format(json_data[0])
            if field_name_errors:
                st.error(f"Improperly Named Fields: {', '.join(field_name_errors)}")
            else:
                st.success("Field names format is valid.")

            empty_columns = find_missing_data(df)
            if empty_columns:
                st.warning(f"Empty Columns Detected: {', '.join(empty_columns)}")

            st.write("**Validate Phone Numbers**")
            

            if 'agent_phone_numbers' in df.columns:

                invalid_agent_numbers = validate_numbers(df, 'agent_phone_numbers')
            if not invalid_agent_numbers.empty:
                st.write("### Invalid Agent Phone Numbers:")
                st.dataframe(invalid_agent_numbers)
            else:
                st.success("All Agent Phone Numbers are valid.")

            if 'office_phone_numbers' in df.columns:
                invalid_office_numbers = validate_numbers(df, 'office_phone_numbers')

            if not invalid_office_numbers.empty:
                st.write("### Invalid Office Phone Numbers:")
                st.dataframe(invalid_office_numbers)
            else:
                st.success("All Office Phone Numbers are valid.")



            st.write("**Dataset Overview**")
            st.dataframe(df)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
