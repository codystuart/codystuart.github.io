"""
Author: Cody Stuart
Project: CS-499 Enhancement 3 - Databases
This python module is being used to create MongoDB environment necessary to enhance the original code to use aggregation pipelines.
"""
import pandas as pd
from pymongo import MongoClient

def setup_database(csv_file_path):
    # MongoDB info
    HOST = 'localhost'
    PORT = 27017
    DB_NAME = 'aac'
    COLLECTION_NAME = 'animals'

    # MongoDB Creds to be used for pulling information from the database. In a real environment this would not be hardcoded.
    USER = 'aacuser'
    PASSWORD = 'verySecurePassword'

    try:
        client = MongoClient(f'mongodb://{HOST}:{PORT}/')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        try:
            db.command("createUser", USER, pwd=PASSWORD, roles=[{"role": "readWrite", "db": DB_NAME}])
            print(f"User '{USER}' created successfully with readWrite permissions on '{DB_NAME}'.")
        except Exception as e:
            if "already exists" in str(e):
                print(f"User '{USER}' already exists. Skipping creation.")
            else:
                raise e

        print(f"Reading data from {csv_file_path}...")
        df = pd.read_csv(csv_file_path)

        data_dict = df.to_dict(orient='records')

        collection.delete_many({})
        print("Existing collection cleared.")

        result = collection.insert_many(data_dict)

        print(f"Successfully created local database '{DB_NAME}' and collection '{COLLECTION_NAME}'.")
        print(f"Inserted {len(result.inserted_ids)} documents.")

    except Exception as e:
        print(f"An error occured during database setup: {e}")

if __name__ == "__main__":
    setup_database('aac_shelter_outcomes.csv')