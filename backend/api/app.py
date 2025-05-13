from flask import Flask, jsonify
import pandas as pd
from backend.handlers.mongo_handler import MongoHandler
from backend.models.document import Document
from backend.documents_list import list_of_documents_lotes, list_of_documents_apartamentos
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask("Living-IA")
CORS(app)

handler = MongoHandler('mongodb+srv://filipedaniel2004:LIA123@lia.xqp0e.mongodb.net/', 'living_datas')

@app.route('/data')
def get_data():
    df = pd.DataFrame({'Nome': ['Alice', 'Bob'], 'Idade': [25, 30]})
    return jsonify(df.to_dict(orient='records'))

@app.route('/mongo')
def get_connection():
    try:
        handler.connect()
        return jsonify({"message": "Connection successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/get/lotes')
def get_data_mongo_lotes():
    try:
        data = str (handler.get_collection("lotes"))
        if data is None:
            return jsonify({"error": "Collection not found or empty"}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/get/apartamentos')
def get_data_mongo_apartamentos():
    try:
        data = str (handler.get_collection("apartamentos"))
        if data is None:
            return jsonify({"error": "Collection not found or empty"}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/insert/lotes', methods=['POST'])
def insert_data_mongo_lotes():
    try:
        data = Document(
            valor="249.000,00",
            localizacao="Centro - Americana",
            tipologia="Loteamento",
            area_m_quadrados="300",
            preco_m="999"
        )
        data = data.to_dict()
        handler.insert("lotes", data)
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/insert/apartamentos', methods=['POST'])
def insert_data_mongo_apartamentos():
    try:
        data = Document(
            valor="1.500.000,00",
            localizacao="Centro - Americana",
            tipologia="Apartamento",
            area_m_quadrados="100",
            preco_m="15000"
        )
        data = data.to_dict()
        handler.insert("apartamentos", data)
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/insert_all/lotes', methods=['POST'])
def insert_all_data_mongo_lotes():
    try:
        for i in range(len(list_of_documents_lotes)):
            data = list_of_documents_lotes[i].to_dict()
            handler.insert("lotes", data)

        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/insert_all/apartamentos', methods=['POST'])
def insert_all_data_mongo_apartamentos():
    try:
        for i in range(len(list_of_documents_apartamentos)):
            data = list_of_documents_apartamentos[i].to_dict()
            handler.insert("apartamentos", data)

        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
## Testando as rotas
    
USERS = [
    {"name": "Test User", "email": "teste@teste.com", "password": "123456"}
]

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = next((u for u in USERS if u["email"] == data["email"] and u["password"] == data["password"]), None)
    if user:
        return jsonify({"success": True, "user": {"name": user["name"], "email": user["email"]}})
    return jsonify({"success": False, "message": "Usuário ou senha inválidos"}), 401

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if any(u["email"] == data["email"] for u in USERS):
        return jsonify({"success": False, "message": "Email já cadastrado"}), 400
    USERS.append({"name": data["name"], "email": data["email"], "password": data["password"]})
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)