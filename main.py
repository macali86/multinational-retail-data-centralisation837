import pandas as pd
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_util import DatabaseConnector
from sqlalchemy import create_engine

# Initialize data extraction and cleaning classes
data_extractor = DataExtractor()
data_cleaning = DataCleaning()

# Initialize database connector
db_connector = DatabaseConnector()

# Connect to the database
engine = db_connector.init_db_engine()

# Verify that the engine is not None
if engine is None:
    raise Exception('Invalid database connection')

# Extract user data from RDS table
df_users = data_extractor.read_rds_table(engine, 'legacy_users')
# Clean user data
data_cleaning.clean_user_data(df_users)
# Upload cleaned user data
db_connector.upload_to_db(df_users, 'dim_users')

# Extract card data from pdf
df_card_details = data_extractor.retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")
# Clean card data
data_cleaning.clean_card_data(df_card_details)
# Upload cleaned card data
db_connector.upload_to_db(df_card_details, 'dim_card_details')

# Extract stores data from API
df_stores_data = data_extractor.retrieve_stores_data()
# Clean stores data
data_cleaning.clean_store_data(df_stores_data)
# Upload cleaned store data
db_connector.upload_to_db(df_stores_data, 'dim_store_details')

# Extract products data from S3 bucket
df_product_details = data_extractor.extract_from_s3("s3://data-handling-public/products.csv")
# Clean products data
data_cleaning.cleaned_products_data(df_product_details)
# Upload cleaned product data
db_connector.upload_to_db(df_product_details, 'dim_products')

# Extract orders data from RDS
df_orders = data_extractor.read_rds_table(engine, 'orders_table')
# Clean orders data
data_cleaning.clean_orders_data(df_orders)
# Upload cleaned orders data
db_connector.upload_to_db(df_orders, 'orders_table')

# Extract date events data from json
df_date_details = data_extractor.extract_from_json()
# Clean date events data
data_cleaning.clean_date_events(df_date_details)
# Upload cleaned date events data
db_connector.upload_to_db(df_date_details, 'dim_date_times')

# Close the database connection
engine.dispose()






