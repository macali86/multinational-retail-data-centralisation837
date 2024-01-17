# multinational-retail-data-centralisation837

## This is a ETL project for the AICore online course, it is a step by step project which is aimed at showcasing the Python and SQL skills that we have been taught and applying them to a real world scenario.

### Softwares Used;
### - Python 3.0
### - PGAdmin4
### - VSCode

### Python Modules:
### - Pandas
### - sqlalchemy
### - tabula
### - boto3
### - BytesIO
### - numpy
### - datetime
### - requests

### The first task is to set up our dev environment, this includes creating a GitHub repo and having the correct softwares installed, they include Python 3.0, PGAdmin4 and VSCode.

### Milestone 2
### - The first task was to create a database in PGADmin4 called sales_data, this is where all the compan data would be stored.

### - The second task to complete was to create 3 python scripts that would contain classes to complete certain actions. The first was data_extraction.py which would contain the class DataExtractor, the next was database_utils.py which contains that class DatabaseCOnnector and finally data_cleaning.py which contains the class DataCleaner.

### - This was as multi-step task that involved a lot of work, the objective was to extract information from a AWS RDS database. I did this by firstly creating a db_creds.yaml this contained the relevant credentials inforamtion to connect to the database.

### - After doing this I created 2 methods in the DatabaseConnector one was to read db_creds.yaml and the other a engine to connect to the AWS RDS database.

### - Then we create a method in the DatabaseConnector that uses the engine and lists the tables, finally we create a method called read_rds_table and pass the needed table as an argument to return the required dataframe.

### - Finally I had to write the relevant data cleaning codes in the DataCleaner under clean_user_data and then upload the cleaned data by creating the connect_to_db and upload_to_db methods in DatabaseConnector class.

### The rest of Milestone 2 involved doin the same processes but each extraction was from a different source they included;
### Card Data - Pdf file
### Store Data - API
### Product Data - S3 Bucket
### Orders Table - AWS RDS Database
### Date Events Data - JSON

### To complete the tasks a number techniques and modules has to be used, which included boto3 and tabula-py.

### Problems & Difficulties
### I encountered a number of problems and difficulties whilst doing these tasks, firstly having to remember the sheer amount of knowledge that had previously been learnt and finding the correct parts of the course to get relevent information was time consuming. Also visualising what the code was going to look and how it was going all connect was another problem for me. Being the first time doing a project like this I struggled to see how it would all come together which made it hard for me to see what I need to do.

### I also has problems seeing where my code was working properly or not I made mistakes in trying to code as much as possible and then running everything at once, If I had to redo this I would use Jupyter notebook and run the code cell by cell.

### Milestone 3
### This Milestone was based arounf PGAdmin4 and using SQL Queries to peform certain tasks.
### First I had to cast the columns of each table to the correct datatypes, these included VARCHAR, DATE, UUID, FLOAT, SMALLINT and BOOL, there were 6 tables to go through.
### Another part of this Milestone was to create primary keys and foreign keys. There would be one main table (orders_table) that would have the foreign keys and link to all the other tables, creating a star-based schema.

### Problems & Difficulties
### I encountered many problems whilst doing this, the first set of problems arose when trying to change datatypes, I was receing SQL errors that certain rows contained values that could not be converted, this meant that my Data Cleaning methods were not correct, I had to go back on a number of occasions and rewrite my data cleaning methods to get rid of any data that had not been cleaned properly. To help with this, I converted all the data i had initially extracted into csv files and also used csv viewer on VSCode so I could which data was bad and the mehtods I could use to clean it.
### The second problem I encountered was when adding the foreign keys, there were some values that were present in one table, but not in the other, again it related to my data cleaning method which had to be revised.

### Milestone 4
### The final part of the project involved using SQL queries to return results that can be used to make decisions, it uses the star-based schema to help make business decisons that can help add value to the overall business.
    # azure-database-migration124
