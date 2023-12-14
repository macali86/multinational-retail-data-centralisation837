import pandas as pd
from data_extraction import DataExtractor
from sqlalchemy import create_engine
from dateutil.parser import parse
import re

# The DataCleaning Class is used to conatin all the methods that will carry out the data cleaning for the data that is extracted 

class DataCleaning:

    """This mehtod is used to clean the data that has been extracted from the RDS for the table named 'Legacy_Users"""

    def clean_user_data(self, df):

        # drop index column
        if "index" in df.columns:
            df = df.drop("index", axis=1)

        """ To clean the date of birth column a lambda function has been created, the lamda function checks for the pattern "YYYY-MM-DD"". It then
            removes any rows where date of birth is missing or doesn't match the pattern, finally it converts it into a datetime format"""

        df["date_of_birth"] = df["date_of_birth"].apply(lambda x: x if re.match(r"\d{4}-\d{2}-\d{2}", str(x)) else pd.NA)
        df = df[df["date_of_birth"].notna()]
        df["date_of_birth"] = pd.to_datetime(df["date_of_birth"])

        """ The same cleaning methods are applied to the join_date column"""

        df["join_date"] = df["join_date"].apply(lambda x: x if re.match(r"\d{4}-\d{2}-\d{2}", str(x)) else pd.NA)
        df = df[df["join_date"].notna()]
        df["join_date"] = pd.to_datetime(df["join_date"])

        return df

    """ This method is used to clean the card data that has been extracted from the pdf"""

    def clean_card_data(self, df):
        
        """ This method drops any rows where the card numbers contain ?"""
        def drop_rows_with_invalid_card_numbers(df):
            return df[~df["card_number"].astype(str).str.contains("\?", regex=True)]

        """ The above function is applied and reurned as df"""
        df = drop_rows_with_invalid_card_numbers(df)   

        """ The same lamda function and changing to datetime functions are used as is in the clean_user_data and clean_card_data methods"""

        df["date_payment_confirmed"] = df["date_payment_confirmed"].apply(lambda x: x if re.match(r"\d{4}-\d{2}-\d{2}", str(x)) else pd.NA)
        df = df[df["date_payment_confirmed"].notna()]
        df["date_payment_confirmed"] = pd.to_datetime(df["date_payment_confirmed"])

        return df
    
    """ This method will clean the data from the data we extracted from API"""

    def clean_store_data(self, df):
        #drop index column
        if "index" in df.columns:
            df_cleaned = df.drop("index", axis=1)

        """ We have created a copy of the original to not affect the original dataframe"""
        cleaned_data = df_cleaned.copy()

        """ We have used pd.to_datetime to convert the data into datetime"""

        cleaned_data['opening_date'] = pd.to_datetime(cleaned_data['opening_date'], errors='coerce')
        cleaned_data['latitude'] = pd.to_numeric(cleaned_data['latitude'], errors='coerce')
        cleaned_data['longitude'] = pd.to_numeric(cleaned_data['longitude'], errors='coerce')
        cleaned_data['lat'] = pd.to_numeric(cleaned_data['lat'], errors='coerce')
        cleaned_data['staff_numbers'] = pd.to_numeric(cleaned_data['staff_numbers'], errors='coerce')

        """ Handle missing values """

        cleaned_data = cleaned_data.dropna(subset=['latitude', 'longitude'], how='any')

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

        # Drop any rows with missing value
        df.dropna(inplace=True)

        """Here we are going through each row where the column ends in 'kg', 'g' or 'ml' and apply the convert_units method"""

        df = df[df["weight"].str.endswith(("kg","g","ml"))]
        df["weight"] = df["weight"].apply(convert_units)
        df_cleaned = df.drop(columns=['Unnamed: 0'], errors='ignore')

        """ This cleaning the 'weight' column into numerics and the 'date_added' column into datetime format."""
        df_cleaned['weight'] = pd.to_numeric(df_cleaned['weight'], errors='coerce')
        df_cleaned['date_added'] = pd.to_datetime(df_cleaned['date_added'], errors='coerce')
        df_cleaned.index = df_cleaned["product_name"]

        print(df_cleaned)

    """ This method cleans all the data that is extracted from the orders_table which is in the RDS"""

    def clean_orders_data(self, orders_table):

        # Drop unnecessary columns: first_name, last_name, and 1
        orders_table.drop(['first_name', 'last_name', '1'], axis=1, inplace=True)

        """ Here we are renaming 2 of the columns in the orders_table, 'order_id' and 'order_date' have been changed to match other tables"""

        orders_table.rename(columns={'order_id': 'order_number', 'order_date': 'order_placed_date_time'}, inplace=True)

        return orders_table
    
    """ This method is used to clean the data that was extracted from the JSON file"""

    def clean_date_events(self, df_events):
        
        """ The columns in the dataframe have had their datatypes changed, some have been changed to numerics and the others to datetime depending on the 
            row name and type of data in the dataframe."""
        df_events['timestamp'] = pd.to_datetime(df_events['timestamp'], errors='coerce')
        df_events['month'] = pd.to_datetime(df_events['month'], format='%B', errors='coerce').dt.month
        df_events['year'] = pd.to_numeric(df_events['year'], errors='coerce')
        df_events['day'] = pd.to_numeric(df_events['day'], errors='coerce')
        df_events['time_period'] = pd.to_datetime(df_events['time_period'], format='%H:%M:%S', errors='coerce').dt.time
        df_events['date_uuid'] = pd.to_datetime(df_events['date_uuid'], errors='coerce')

       """ This is to drop any rows that do not contain any timestamo values"""
        df_events = df_events.dropna(subset=['timestamp'])

        return df_events
