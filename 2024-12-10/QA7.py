import streamlit as st
import json
import re

# Mandatory fields for validation
mandatory_fields = [
    "first_name", "image_url", "address", "city",
    "state", "zipcode", "office_phone_numbers",
    "agent_phone_numbers", "profile_url"
]

# All fields in the schema
all_fields = [
    "first_name", "middle_name", "last_name", "office_name", "title",
    "description", "languages", "image_url", "address", "city", "state",
    "country", "zipcode", "office_phone_numbers", "agent_phone_numbers",
    "email", "website", "social", "profile_url"
]

# Correct spelling of fields to check for
correct_fields = {
    "first_name": "first_name", "middle_name": "middle_name", "last_name": "last_name", 
    "office_name": "office_name", "title": "title", "description": "description", 
    "languages": "languages", "image_url": "image_url", "address": "address", 
    "city": "city", "state": "state", "country": "country", "zipcode": "zipcode", 
    "office_phone_numbers": "office_phone_numbers", "agent_phone_numbers": "agent_phone_numbers",
    "email": "email", "website": "website", "social": "social", "profile_url": "profile_url"
}

# Regex patterns for validation
url_pattern = r"https?://[^\s]+"  # Basic URL regex
phone_pattern = r"^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"  # US phone number pattern
email_pattern = r"^[a-zA-Z0-9_.+\-']+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"  # Email pattern

# Sidebar for file upload
st.sidebar.title("Upload JSON File")
uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type=["json"])

if uploaded_file:
    st.sidebar.success("✅ File uploaded successfully!")
    
    try:
        # Load JSON file
        data = json.load(uploaded_file)
        st.title("Enhanced JSON QA Dashboard with Email Validation")
        
        # File Structure Validation
        if isinstance(data, list):
            st.success("✅ JSON is a valid list of objects.")
            
            # Initialize trackers for issues
            missing_field_issues = []
            invalid_url_issues = []
            invalid_phone_issues = []
            invalid_email_issues = []
            spelling_issues = []
            processed_data = []
            unique_states = set()
            unique_countries = set()
            
            # Iterate through records for validation
            for i, record in enumerate(data):
                processed_record = {}
                
                # Check for null values in specified fields and replace with empty string
                for field in ["middle_name", "last_name", "description", "address", "city", "state", "zipcode"]:
                    if field in record and (record[field] is None or record[field] == ""):
                        record[field] = ""  # Replace null or empty values with empty string

                # Check for missing mandatory fields
                for field in mandatory_fields:
                    if field not in record or not record[field]:
                        missing_field_issues.append({"Record Index": i + 1, "Field": field, "Value": record.get(field)})
                
                # Check URLs
                for field in ["image_url", "profile_url", "website"]:
                    if field in record and record[field] and not re.match(url_pattern, record[field]):
                        invalid_url_issues.append({"Record Index": i + 1, "Field": field, "Value": record[field]})
                
                # Check Phone Numbers
                for field in ["agent_phone_numbers", "office_phone_numbers"]:
                    if field in record:
                        for phone in record[field]:
                            if not re.match(phone_pattern, phone):
                                invalid_phone_issues.append({"Record Index": i + 1, "Field": field, "Phone": phone})
                
                # Check Emails
                if "email" in record and record["email"] and not re.match(email_pattern, record["email"]):
                    invalid_email_issues.append({"Record Index": i + 1, "Field": "email", "Email": record["email"]})
                
                # Check Spelling for all fields
                for field in record:
                    if field not in correct_fields:
                        spelling_issues.append({"Record Index": i + 1, "Incorrect Field": field})
                
                # Add unique values for state and country
                if "state" in record and record["state"]:
                    unique_states.add(record["state"])
                if "country" in record and record["country"]:
                    unique_countries.add(record["country"])
                
                # Replace null values in optional fields with empty strings
                for field in all_fields:
                    processed_record[field] = record.get(field, "") if record.get(field) is not None else ""
                
                processed_data.append(processed_record)
            
            # Display Results
            st.subheader("Validation Results")
            
            if missing_field_issues:
                st.error("❌ Missing values detected in mandatory fields:")
                st.json(missing_field_issues)
            else:
                st.success("✅ All mandatory fields are present and non-null.")
            
            if invalid_url_issues:
                st.error("❌ Invalid URLs detected:")
                st.json(invalid_url_issues)
            else:
                st.success("✅ All URLs are valid.")
            
            if invalid_phone_issues:
                st.error("❌ Invalid phone numbers detected:")
                st.json(invalid_phone_issues)
            else:
                st.success("✅ All phone numbers are valid.")
            
            if invalid_email_issues:
                st.error("❌ Invalid email addresses detected:")
                st.json(invalid_email_issues)
            else:
                st.success("✅ All email addresses are valid.")
            
            if spelling_issues:
                st.error("❌ Incorrect field names detected:")
                st.json(spelling_issues)
            else:
                st.success("✅ All fields are correctly spelled.")
            
            # Show unique states and countries
            st.subheader("Unique Values in 'state' and 'country' Columns")
            st.write(f"Unique states: {list(unique_states)}")
            st.write(f"Unique countries: {list(unique_countries)}")
            
            # Provide Download Option for Processed Data
            st.subheader("Processed Data")
            st.write("All null values in specified fields have been replaced with empty strings.")
            st.json(processed_data)
            
            # Download button for processed JSON
            st.download_button(
                label="Download Processed JSON",
                data=json.dumps(processed_data, indent=4),
                file_name="processed_data.json",
                mime="application/json"
            )
        
        else:
            st.error("❌ JSON file should be a list of objects.")
    
    except json.JSONDecodeError:
        st.error("❌ Unable to parse JSON. Please check the file format.")
