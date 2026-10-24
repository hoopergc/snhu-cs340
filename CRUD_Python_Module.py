# Example Python Code to Insert a Document
# Additional code by G.C. Hooper
# Date submitted: Sunday, October 4th, 2026
# CS-340-13407-M01
# Modified to not use self coded values for use in 5-2 assignment

from pymongo import MongoClient 
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 
    # Modified to include parameters for username, password, host, port, database, and collection
    # rather than hard coded values
    def __init__(self, USER, PASS, HOST, PORT, DB, COL): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        #USER = 'aacuser' 
        #PASS = 'fringe uneasy festival outpour swimmable' # Set to new password
        #HOST = 'localhost' 
        #PORT = 27017 
        #DB = 'aac' 
        #COL = 'animals' 
        self.USER = USER
        self.PASS = PASS
        self.HOST = HOST
        self.PORT = PORT
        self.DB = DB
        self.COL = COL
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if type(data) is not dict:
            raise ValueError("data parameter must be of type dictionary") # raise excpetion if data is not dictionary
        elif data is None: 
            raise ValueError("Nothing to save, because data parameter is empty")  # Raise exception for empty data parameter
        else:
            try:  # Try to insert data into animals
                result = self.database.animals.insert_one(data)  # data should be dictionary             
                return result.acknowledged # return True upon successful insert
            except PyMongoError: # Return False if create operation fails
                return False

    # Create method to implement the R in CRUD.
    def read(self, query):
        if type(query) is not dict:  # query must be of type dictionary
            raise ValueError("query parameter must be of type dictionary")
        elif query is None:  # Query cannot be empty
            raise ValueError("query parameter cannot be empty")
        else:
            try:  # try to run find operation with query
                return list(self.collection.find(query))  # return query as list
            except PyMongoError:  # return empty list if error occurs
                return []
    
    # Create method to implement the U in CRUD
    # Includes document paremeter for documents to update and data parameter for new data
    def update(self, document, data): 
        # Raise exception if parameters are not of dictionary type
        if type(document) is not dict or type(data) is not dict:
            raise ValueError("query must be a dictionary")
        elif data is None or document is None:  # Raise exception if document or data is empty
            raise ValueError("Query cannot be empty")
        else:
            try:
                result = self.collection.update_many(document, data)  # Result of updateMany
                return result.matched_count # Return number of documents updated
            except PyMongoError:
                return 0
    
    # Create method to implement the D in CRUD
    def delete(self, data):
        if type(data) is not dict:  # Raise exception is data is not dictionary
            raise ValueError("data must be of type dictionary")
        elif data is None:  # Raise exception is data parameter is empty
            raise ValueError("data cannot be empty")
        else:
            try:  # Attempt to delete documents matching data query
                result = self.collection.delete_many(data)  # Result of deleteMany on collection
                return result.deleted_count  # Return number of deleted objects
            except PyMongoError:  # Return 0 in event on PyMongo Error
                return 0