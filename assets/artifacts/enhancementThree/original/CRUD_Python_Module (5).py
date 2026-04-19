# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): # Get username and password as parameters.
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        # USER = 'aacuser'
        # PASS = 'verySecurePassword' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (username,password,HOST,PORT)) 
            self.database = self.client['%s' % (DB)] 
            self.collection = self.database['%s' % (COL)]
            print("Connection to MongoDB successful!")
        except Exception as e:
            print(f" Could not connect to MongoDB: {e}")

    def aggregate(self, pipeline):
        if pipeline is not None:
            try:
                cursor = self.collection.aggregate(pipeline)
                return list(cursor)
            except Exception as e:
                print(f"An error occured during aggregation: {e}")
                return []
        else:
            raise Exception("Pipeline parameter is required for aggregation.")

    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        """
        Inserts a document into the 'animals' collection
        @param data: A dictionary representing the document to insert.
        @return: True if the insert was successful, otherwise False.
        """
        if data is not None: # validate paramters being passed in have actual values.
            try:
                result = self.database.animals.insert_one(data)  # data should be dictionary
                return result.acknowledged # returns True if data is inserted
            except Exception as e:
                print(f"An error occured during insert: {e}")
                return False
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 

    # Create method to implement the R in CRUD.
    def read(self, query):
        """
        Queries for documents in the 'animals' collection.
        @param query: A dictionary defining the search criteria.
        @return: A list of matching documents. Returns an empty list if no matches.
        """
        if query is not None: # validate paramters being passed in have actual values.
            try:
                # The find() method returns a 'cursor' which is a pointer to the results.
                cursor = self.collection.find(query)
                # Convert the cursor to a list to return all matching documents
                results_list = list(cursor)
                return results_list
            except Exception as e:
                print(f"An error occured during read operation: {e}")
                return [] # returns an empty list
            
    def read_water_rescue(self):
        query = {
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)

    def read_water_rescue_optimized(self):
        pipeline = [
            {"$match": {
                "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
                "sex_upon_outcome": "Intact Female",
                "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
            }},
            {"$project": {
                "_id": 0,
                "name": 1,
                "breed": 1,
                "age_upon_outcome_in_weeks": 1,
                "location_lat": 1,
                "location_long": 1
            }}
        ]
        return self.aggregate(pipeline)
    
    def read_mountain_rescue(self):
        query = {
           "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)

    def read_disaster_rescue(self):
        query = {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)

            
    # Update method to implement the U in CRUD.
    def update(self, query, newValues):
        """
        Updates one or more documents matching a query.
        @param query: A dictionary defining the documents to update.
        @param newValues: A dictionary containing the fields and new values to set.
        @return: The number of documents that were modified
        """
        if query is not None and newValues is not None: # validate paramters being passed in have actual values.
            try:
                result = self.collection.update_many(query, {"$set": newValues})
                # Get the number of records modified as the return value
                return result.modified_count
            except Exception as e:
                print(f"An error occured during update: {e}")
                return 0
        else:
            raise Exception ("Query and newValues parameters are required to update.")
    
    # Delete method to implement the D in CRUD.
    def delete(self, query):
        """
        Deletes one or more documents matching a query.
        @param query: A dictionary defining the documents to delete.
        @return: The number of documents deleted. 
        """
        if query is not None: # validate paramters being passed in have actual values.
            try:
                result = self.collection.delete_many(query)
                # return the number of records deleted
                return result.deleted_count
            except Exception as e:
                print(f"An error occured during deletion: {e}")
                return 0 # When delete fails return 0
        else:
            raise Exception("Query paramter is required for deletion.")
