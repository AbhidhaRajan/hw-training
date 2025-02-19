import pandas as pd


file_path = "/home/abhidha/Downloads/DataHut_AT_Mueller_FullDump_20250220.CSV"
df = pd.read_csv(file_path,delimiter='|')

price_columns = ["regular_price","selling_price","promotion_price","price_was"]



comma_prices = pd.DataFrame()


for col in price_columns:
    filtered_rows = df[df[col].astype(str).str.contains(',', na=False)]
    comma_prices = pd.concat([comma_prices, filtered_rows])


if not comma_prices.empty:

    print("Rows with commas in price columns found.")
    comma_prices.to_excel("comma_price_rows.xlsx", index=False, engine='openpyxl')
    print("Filtered rows saved to 'comma_price_rows.xlsx'.")
else:
    print("No rows with commas found in the price columns.")
