import logging
from pymongo import MongoClient

#Modelo de query no mongo : db.collection.find({field:value}) -- pode ser find, insert, delete ou update

#Classe MongoHandler para manipulação do banco de dados MongoDB
class MongoHandler:
    #Metodo construtor da classe
    def __init__(self, connection_string = None, database_name = "test"):
        if connection_string is None:
            self.connection_string = 'mongodb+srv://filipedaniel2004:LIA123@lia.xqp0e.mongodb.net/?retryWrites=true&w=majority&appName=LIA' #Inserir string de conexão do mongoDB
        else:
            self.connection_string = connection_string

        self.database_name = database_name

    #Metodo de conexão com o banco de dados
    def connect(self):
        return MongoClient(self.connection_string).get_database(self.database_name)


    def insert(self, collection, data):
        db = self.connect() #usa o metodo connect para criar um objeto db
        if db is None or not collection in db.list_collection_names():
            return False
        try:
            db.get_collection(collection).insert_one(data) #insere um documento na coleção
        except:
            logging.error(f"Error inserting data into collection {collection}")
            return False
        finally:
            db.close()
            return True

    def get_collection (self, collection):
        db = self.connect()
        if db is None or not collection in db.list_collection_names():
            return False
        try:
            exportedCollection = db.get_collection(collection).find()
        except:
            logging.error(f"Error getting data from collection {collection}")
            return False
        finally:
            db.close()
            return exportedCollection

    def get_data(self, collection, field, value):
        db = self.connect()
        if db is None or not collection in db.list_collection_names():
            return False
        try:
            exportedDatas = db.get_collection(collection).find({field:value})
        except:
            logging.error(f"Error getting data from collection {collection} with value: {value}")
            return False
        finally:
            db.close()
            return exportedDatas

    def delete_data(self, collection, field, value):
        db = self.connect()
        if db is None or not collection in db.list_collection_names():
            return False
        try:
            db.get_collection(collection).delete_one({field:value})
        except:
            logging.error(f"Error deleting data from collection {collection} with value: {value}")
            return False
        finally:
            db.close()
            return True

    def update_data(self, collection, field, value, new_data):
        db = self.connect()
        if db is None or not collection in db.list_collection_names():
            return False
        try:
            db.get_collection(collection).update_one({field:value}, new_data)
        except:
            logging.error(f"Error updating data from collection {collection} - {field}: {value} with new data: {new_data}")
            return False
        finally:
            db.close()
            return True