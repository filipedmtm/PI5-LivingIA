import logging
from pymongo import MongoClient

class MongoHandler:
    def __init__(self, connection_string=None, database_name="living_datas"):
        if connection_string is None:
            self.connection_string = 'mongodb+srv://filipedaniel2004:LIA123@lia.xqp0e.mongodb.net/?retryWrites=true&w=majority&appName=LIA'
        else:
            self.connection_string = connection_string

        self.database_name = database_name
        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database(self.database_name)

    def connect(self):
        try:
            self.db = MongoClient(self.connection_string).get_database(self.database_name)
            return True
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            return False

    def close_connection(self):
        self.client.close()

    # def insert(self, collection, data):
    #     if collection not in self.db.list_collection_names():
    #         return None
    #     try:
    #         self.db.get_collection(collection).insert_one(data)
    #         return True
    #     except Exception as e:
    #         logging.error(f"Error inserting data into collection {collection}: {e}")
    #         return None

    def insert(self, collection, data):
        try:
            self.db.get_collection(collection).insert_one(data)
            return True
        except Exception as e:
            logging.error(f"Error inserting data into collection {collection}: {e}")
            return None

    def get_collection(self, collection):
        if collection not in self.db.list_collection_names():
            return None
        try:
            return list(self.db.get_collection(collection).find())
        except Exception as e:
            logging.error(f"Error getting data from collection {collection}: {e}")
            return None

    # def get_data(self, collection, field, value):
    #     if collection not in self.db.list_collection_names():
    #         return None
    #     try:
    #         return list(self.db.get_collection(collection).find({field: value}))
    #     except Exception as e:
    #         logging.error(f"Error getting data from collection {collection} with value {value}: {e}")
    #         return None

    def get_data(self, collection, field, value):
        try:
            col = self.db.get_collection(collection)
            if col is None:
                return []

            result = list(col.find({field: value}))
            return result
        except Exception as e:
            logging.error(f"Erro ao buscar dados da coleção {collection}: {e}")
            return []

    def delete_data(self, collection, field, value):
        if collection not in self.db.list_collection_names():
            return None
        try:
            self.db.get_collection(collection).delete_one({field: value})
            return True
        except Exception as e:
            logging.error(f"Error deleting data from collection {collection} with value {value}: {e}")
            return None

    def update_data(self, collection, field, value, new_data):
        if collection not in self.db.list_collection_names():
            return None
        try:
            self.db.get_collection(collection).update_one({field: value}, {"$set": new_data})
            return True
        except Exception as e:
            logging.error(f"Error updating data in collection {collection} - {field}: {value} with new data: {new_data}: {e}")
            return None
        finally:
            self.client.close()