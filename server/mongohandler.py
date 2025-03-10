import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class MongoHandler:
    def __init__(self, connection_string=None, database_name=None):
        # Se não for passada connection_string, buscar do .env
        if not connection_string:
            connection_string = os.getenv("MONGO_URI", "mongodb://localhost:27017")

        # Se não for passado database_name, buscar do .env
        if not database_name:
            database_name = os.getenv("DB_NAME", "test")

        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[database_name]

    async def insert(self, collection, data: dict):
        """
        Insere um único documento em uma coleção.
        Retorna o ID inserido ou None em caso de erro.
        """
        try:
            result = await self.db[collection].insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            logging.error(f"Error inserting data into collection {collection}: {e}")
            return None

    async def get_collection(self, collection):
        """
        Retorna todos os documentos de uma coleção como lista.
        """
        try:
            cursor = self.db[collection].find()
            docs = await cursor.to_list(length=1000)  # Ajuste o length conforme necessidade
            return docs
        except Exception as e:
            logging.error(f"Error getting data from collection {collection}: {e}")
            return None

    async def get_data(self, collection, field, value):
        """
        Retorna documentos filtrados {field: value}.
        """
        try:
            cursor = self.db[collection].find({field: value})
            docs = await cursor.to_list(length=1000)
            return docs
        except Exception as e:
            logging.error(f"Error getting data from {collection} with {field}={value}: {e}")
            return None

    async def delete_data(self, collection, field, value):
        """
        Deleta um documento que corresponde ao {field: value}.
        Retorna True se der certo, False se falhar.
        """
        try:
            await self.db[collection].delete_one({field: value})
            return True
        except Exception as e:
            logging.error(f"Error deleting data from collection {collection}: {e}")
            return False

    async def update_data(self, collection, field, value, new_data):
        """
        Atualiza um documento que corresponde ao {field: value} com new_data.
        Retorna True se der certo, False se falhar.
        """
        try:
            await self.db[collection].update_one({field: value}, {"$set": new_data})
            return True
        except Exception as e:
            logging.error(f"Error updating data in collection {collection}: {e}")
            return False
