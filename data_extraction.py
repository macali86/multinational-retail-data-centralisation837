import csv
import pandas as pd
import tabula
from database_util import DatabaseConnector
import requests
import json
import boto3
import sqlalchemy
from io import BytesIO

# Create a Class named DataExtractor that will include all the methods to extract data from different sources

class DataExtractor:

    def __init__(self):
        pass

    """"This method takes in the engine that was created in the init_db_engine method from the Database Connector class to connect to
        the RDS that contains the table, then uses pandas function .read_sql_table to return the dataframe"""

    def read_rds_table(self, engine, table_name):
        df = pd.read_sql_table(table_name, engine)
        return df

    """"This method takes in a link that contains data stored as a pdf, it the uses tabula.read_pdf to read all the pages, the we use pd.concat
        to concatenate a list of Dataframes, ignore_index=True parameter is used to create a new index and join="inner" is used to only include
        common columns"""

    def retrieve_pdf_data(self, link, csv_filename="pdf_data.csv"):
        all_pages = tabula.read_pdf(link, pages="all")
        df_pdf = pd.concat(all_pages, ignore_index=True, join="inner")

        # Convert data into csv file to make it easier to read
        df_pdf.to_csv(csv_filename, index=False)
        return df_pdf

    """"This method contains the API key"""

    def API(self):
        return {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
    

    """"This method is used to connect to the url and use the API key method to list the number of stores. we use the requests.get function
        and pass the url and API. We use pd.Dataframe funcion to create a dataframe. The response.json is used to parse the content as json in the key
        number_of_stores"""

    def list_number_of_stores(self, csv_filename="number_of_stores.csv"):
        url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
        response = requests.get(
                                url,
                                headers=self.API()
                                )
        df = pd.DataFrame({"number_of_stores": [response.json()['number_stores']]})

        # Convert data into csv file to make it easier to read
        df.to_csv(csv_filename, index=False)
        return response.json()['number_stores']
    
    """"This method is used to retrieve details using a API, first it creates a empty list to store Dataframes, then it gets the total
        number of stores using self.list_number_of_stores, then it loops through using a for statement. A GET request is made the API
        and normalize the JSON response, finally everything is concatentated"""

    def retrieve_stores_data(self, csv_filename="stores_data.csv"):
        list_of_frames = []
        store_number   = self.list_number_of_stores()
        for _ in range(store_number):
            url = f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{_}'
            response = requests.get(
                                    url,
                                    headers=self.API()
                                    )
            list_of_frames.append( pd.json_normalize(response.json()))
        df = pd.concat(list_of_frames)

        # Convert data into csv file to make it easier to read
        df.to_csv(csv_filename, index=False)
        return df

    """"This method is used to extract data from a S3 bucket, firstly we use boto3 to create a S3 client. We split the address to the bucket name 
        and key. We use .get_object to retrieve the data fron the specified  object, then we read the body and convert it into a file like object"""

    def extract_from_s3(self, s3_address, csv_filename="products.csv"):
        s3_client = boto3.client('s3')
        bucket_name, key = s3_address.split('/')[2:]
        response = s3_client.get_object(Bucket="data-handling-public", Key="products.csv")
        content = response['Body'].read()
        file_like_object = BytesIO(content)

        # Convert data into csv file to make it easier to read
        df = pd.read_csv(file_like_object)

        return df

    """"This method is used to connect to URL and then extract datat from a JSON file. Firstly we have to define the URL and make a GET request
        We then create a if statement to see if the connection has been made, after this we use json.loads to parse into Python and finally crrate a
        Dataframe"""

    def extract_from_json(self, csv_filename="date_details.csv"):     
        URL="https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
        response = requests.get(URL)

        if response.status_code == 200:
            data = json.loads(response.content)
            df_date_events = pd.DataFrame(data)

            # Convert data into csv file to make it easier to read
            df_date_events.to_csv(csv_filename, index=False)

            return df_date_events
        else:
            raise Exception(f"Error retrieving JSON data: {response.status_code}")