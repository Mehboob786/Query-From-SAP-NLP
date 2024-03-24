import json
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from pandas import read_sql_query
from SAPQureyGen import SAPQureyGenAI

generator_instance = SAPQureyGenAI()

class DBHelper:
    def __init__(self):
        self.db_user = os.environ.get("db_user")
        self.db_password = os.environ.get("db_password")
        self.db_host = os.environ.get("db_host")
        self.db_name = os.environ.get("db_name")
        self.db_password = quote_plus(self.db_password)
        # Updated connection string for pymssql
        self.connection_string = f'mssql+pymssql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'

    def connect_db(self):
        try:
            # Create SQLAlchemy engine
            engine = create_engine(self.connection_string)
            connection = engine.connect()
            return connection
        except SQLAlchemyError as e:
            print(f"Database connection error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def query_db(self, query, attempt=1):
        try:
            connection = self.connect_db()
            if connection:
                # Execute query and return results as DataFrame
                result = read_sql_query(query, connection)
                connection.close()
                return result
        except Exception as e:
            print(f"Attempt {attempt}: Query execution failed: {e}")
            if attempt < 3:
                queryjson = generator_instance.ValidateQureyError(query, e)
                print("queryjson From Error")
                cleaned_str = queryjson.strip('` \n').replace("json\n", "", 1)
                # Convert the JSON string to a Python dictionary
                print("cleaned_str")
                print(cleaned_str)
                response_dict = json.loads(str(cleaned_str))
                # Extract the query from the dictionary
                correctedqurey = response_dict.get('Query', 'No query found.').strip('` \n').replace("sql\n", "", 1).replace("\\n", "\n")
                print("correctedqurey From Error")
                print(str(correctedqurey))
                # Recursively call the function with incremented attempt
                return self.query_db(correctedqurey, attempt + 1)
            else:
                # If 3 attempts are made, return None
                print("Query execution failed after 3 attempts.")
                return None