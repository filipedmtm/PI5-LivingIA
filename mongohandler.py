from pymongo import MongoClient

#Classe MongoHandler para manipulação do banco de dados MongoDB
class MongoHandler:
    #Método construtor da classe
    def __init__(self, connection_string = None, database_name = "test"):
        if connection_string is None:
            self.connection_string = "..." #Inserir string de conexão do mongoDB
        else:
            self.connection_string = connection_string

        self.database_name = database_name

    #Método de conexão com o banco de dados
    def connect(self):
        return MongoClient(self.connection_string).get_database(self.database_name)

