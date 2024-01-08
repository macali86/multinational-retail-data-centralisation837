import pandas as pd
from data_extraction import DataExtractor
from sqlalchemy import create_engine
import numpy as np
import datetime as dt

# The DataCleaning Class is used to conatin all the methods that will carry out the data cleaning for the data that is extracted 

class DataCleaning:

    """ This Method is used to clean the users data that has been extracted after dropping the index it checks the date_of_birth and join_date column
    for any uppercase to or alphanumeric characters by applying a lambda function, it the converts the rest of the columns to datetime using the format mixed
    as some dates are in mixed format and the others to astype"""

    def clean_user_data(self, df):

        # drop index column
        if "index" in df.columns:
            df = df.drop("index", axis=1)
        
        df = df[~df['date_of_birth'].apply(lambda x: x.isupper() and x.isalnum())]
        df = df[~df['join_date'].apply(lambda x: x.isupper() and x.isalnum())]
        df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], format='mixed')
        df["join_date"] = pd.to_datetime(df["join_date"], format='mixed')
        df["country_code"] = df["country_code"].astype("category")
        df["country"] = df["country"].astype("category")
        """ The same cleaning methods are applied to the join_date column"""
        return df

    """ This method is used to clean the card data that has been extracted from the pdf"""

    def clean_card_data(self, df):
        
        """ We drop any rows where the card numbers contain ?"""

        df['card_number'] = df['card_number'].astype(str).str.replace("\?", "", regex=True)
  
        """Here we are converting to a datetime using a lambda function with the format month/year, if the element is not a string it is left unchanged"""

        df['expiry_date'] = df['expiry_date'].apply(lambda x: pd.to_datetime(x, errors='coerce', format='%m/%y') if isinstance(x, str) else x)
        df['date_payment_confirmed'] = df['date_payment_confirmed'].astype("datetime64[as]")

        df_cleaned = df.dropna()

        return df_cleaned

    """ This method will clean the data from the data we extracted from API"""

    def clean_store_data(self, df):

        
        # Drop the "index" column if it exists and drop the lat column
        df_cleaned = df.copy() if "index" in df.columns else df
        df_cleaned = df.drop("lat", axis=1)


        df_cleaned['staff_numbers'] = pd.to_numeric(df_cleaned['staff_numbers'].str.replace(r"[^\d]", "", regex=True), errors='coerce')

        """We are using the same code as in the clean_user_data to check for uppercase and numbers."""
        df_cleaned = df_cleaned[~df_cleaned['opening_date'].apply(lambda x: x.isupper() and x.isalnum())] 

        #Convert specific columns to appropriate data types
        df_cleaned['opening_date'] = pd.to_datetime(df_cleaned['opening_date'], format='mixed')
        df_cleaned['latitude'] = pd.to_numeric(df_cleaned['latitude'], errors='coerce')
        df_cleaned['longitude'] = pd.to_numeric(df_cleaned['longitude'], errors='coerce')
        df_cleaned['staff_numbers'] = pd.to_numeric(df_cleaned['staff_numbers'], errors='coerce')

        cleaned_data = df_cleaned.dropna(subset=['latitude', 'longitude'], how='any')

        return cleaned_data

    """ This method is to clean the data we extracted from S3 Bucket"""

    def cleaned_products_data(self, df):

        """Here we are converting all values into kg, if the value contains a 'x' it recognises it as a multiplication and multiplies the 2 vlaues
            it will also convert any values ending with ml or g into kg."""

        def convert_units(value):
            if "x" in value:
                left, right = value.split("x")
                value = (float(left) * float(right[:-1])) / 1000
                return value
            if value.endswith("kg"):
                return float(value[:-2])
            elif value.endswith("g"):
                return float(value[:-1]) / 1000
            elif value.endswith("ml"):
                return float(value[:-2]) / 1000
            elif value.endswith("oz"):
                return float(value[:-2]) / 35.27396 

        # Drop any rows with missing value
        df.dropna(inplace=True)

        """Here we are going through each row where the column ends in 'kg', 'g', 'ml' or 'oz' and apply the convert_units method"""

        df = df[df["weight"].str.endswith(("kg","g","ml","oz"))]
        df["weight"] = df["weight"].apply(convert_units)
        df_cleaned = df.drop(columns=['Unnamed: 0'], errors='ignore')

        """ This cleaning the 'weight' column into numerics and the 'date_added' column into datetime format."""
        df_cleaned['weight'] = pd.to_numeric(df_cleaned['weight'], errors='coerce')
        df_cleaned['date_added'] = pd.to_datetime(df_cleaned['date_added'], errors='coerce')
        df_cleaned.index = df_cleaned["product_name"]

        print(df_cleaned)
        return df_cleaned

    """ This method cleans all the data that is extracted from the orders_table which is in the RDS"""

    def clean_orders_data(self, orders_table):

        # Drop unnecessary columns: first_name, last_name, and 1
        orders_table.drop(['first_name', 'last_name', '1'], axis=1, inplace=True)

        """ Here we are renaming 2 of the columns in the orders_table, 'order_id' and 'order_date' have been changed to match other tables"""

        orders_table.rename(columns={'order_id': 'order_number', 'order_date': 'order_placed_date_time'}, inplace=True)

        return orders_table
    
    """ This method is used to clean the data that was extracted from the JSON file"""

    

    def clean_date_events(self, df_events):

        """Cleans and transforms date-related columns in the DataFrame, including UUID validation."""

        df_events['timestamp'] = pd.to_datetime(df_events['timestamp'], errors='coerce').dt.time
        df_events['month'] = pd.to_numeric(df_events['month'], errors='coerce')
        df_events['year'] = pd.to_numeric(df_events['year'], errors='coerce')
        df_events['day'] = pd.to_numeric(df_events['day'], errors='coerce')
        df_events['time_period'] = df_events['time_period'].str.upper().where(~df_events['time_period'].str.isupper(), np.nan)
        
        required_characters = 36

        df_events['date_uuid'] = np.where(df_events['date_uuid'].str.len() < required_characters, np.nan, df_events['date_uuid'])
        df_events = df_events.dropna(subset=['date_uuid'])

        return df_events