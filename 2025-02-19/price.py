import pandas as pd

# Load the Excel file 
file_path = "/home/abhidha/Downloads/accessories_02/trunkliners_2025_02_18.xlsx"  
df = pd.read_excel(file_path)

# Define price columns
price_columns = ["Catalogue_price", "Net_price"]


# Create an empty DataFrame to store rows with commas
comma_prices = pd.DataFrame()

 # Loop through price columns to find rows containing commas
for col in price_columns:
    filtered_rows = df[df[col].astype(str).str.contains(',', na=False)]
    comma_prices = pd.concat([comma_prices, filtered_rows])

 # Display and save results
if not comma_prices.empty:

    print("Rows with commas in price columns found.")
    comma_prices.to_excel("comma_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'comma_price_rows.xlsx'.")
else:
    print("No rows with commas found in the price columns.")
