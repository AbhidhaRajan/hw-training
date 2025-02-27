import great_expectations as gx
import pandas as pd

# Load your data into a Pandas DataFrame
df = pd.read_csv("/home/abhidha/Downloads/DataHut_AT_Fressnapf_FullDump_20250227.CSV", delimiter='|',low_memory=False)

# Create a Data Context
context = gx.get_context()

# Create a Datasource
#datasource = context.sources.add_pandas(name="my_pandas_datasource")

# Create a Data Asset
#data_asset = datasource.add_dataframe_asset(name="my_data_asset", dataframe=df)

# Create a new Expectation Suite
expectation_suite = context.add_expectation_suite("my_expectation_suite")

# Add Expectations
data_asset.expect_column_values_to_not_be_null(column_list=[
    "age_of_the_product", "age_recommendations", "alchol_by_volume", "allergens", "barcode", 
    "beer_deg", "brand_type", "care_instructions", "chilled", "competitor_product_key", 
    "cooking_part", "country_of_origin", "dietary_lifestyle", "dimensions", "dosage_recommendation", 
    "drained_weight", "environmental", "features", "fit_guide", "flavour", "food_preservation", 
    "frozen", "grade", "grape_variety", "handmade", "heel_height", "heel_type", "importer_address", 
    "instructionforuse", "instructions", "label_information", "labelling", "manufacturer_address", 
    "material_composition", "max_heating_temperature", "model_number", "multi_buy_item_count", 
    "multi_buy_items_price_total", "multibuy_items_pricesingle", "netweight", "nutritional_information", 
    "nutritions", "occasion", "organictype", "package_sizeof_sellingprice", "packaging", 
    "per_unit_sizedescription", "perfect_match", "preparationinstructions", "price_valid_from", 
    "processed_food", "producthierarchy_level6", "producthierarchy_level7", "promo_limit", 
    "promotion_type", "promotion_valid_from", "promotion_valid_upto", "random_weight_flag", 
    "receipies", "recycling_information", "region", "return_address", "servings_per_pack", 
    "special_information", "standard_drinks", "storage_instructions", "store_addressid", 
    "store_addressline1", "store_addressline2", "store_name", "store_postcode", "store_state", 
    "store_suburb", "style", "suitable_for", "tasting_note", "upc", "usp", "vinification_details", 
    "vitamins", "warranty"
])

# Save the Expectation Suite
data_asset.save_expectation_suite()
