import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
import psycopg2

#Create a class named DatabaseConnector that will contain methods 

class DatabaseConnector:

    def read_db_creds(self, db_creds_file='db_creds.yaml'):
        with open(db_creds_file, 'r') as file:
            x = yaml.safe_load(file)
        return x
    
    def init_db_engine(self):

        creds = self.read_db_creds('db_creds.yaml')

        connection_string = f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"

        engine = create_engine(connection_string)
        return engine

    def list_db_tables(self):

        engine = self.init_db_engine()
        with engine.connect():
            inspector = inspect(engine)
            table_names = inspector.get_table_names()
        return table_names
    
    def connect_to_db(self):
        creds = self.read_db_creds('postgres.yaml')
        connection_params = f"postgresql://{creds['USER']}:{creds['PASSWORD']}@{creds['SERVER']}:{creds['PORT']}/{creds['DATABASE']}"

        engine_postgres = create_engine(connection_params)
        return engine_postgres

    def upload_to_db(self, df, table_name):
        engine_postgres = self.connect_to_db()
        df.to_sql(table_name, engine_postgres, index=False, if_exists='replace')
