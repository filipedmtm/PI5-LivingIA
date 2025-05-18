from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS

# Imports do projeto
from backend.handlers.mongo_handler import MongoHandler
from backend.models.document import Document
from backend.documents_list import list_of_documents_lotes, list_of_documents_apartamentos
from backend.dashboard import init_dashboard

# Inicializa o app Flask
app = Flask("Living-IA")
CORS(app)

# Handler do MongoDB
handler = MongoHandler('mongodb+srv://filipedaniel2004:LIA123@lia.xqp0e.mongodb.net/', 'living_datas')
USERS_COLLECTION = "usuarios"

# -------------------- ROTAS --------------------

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
        data = str(handler.get_collection("lotes"))
        if data is None:
            return jsonify({"error": "Collection not found or empty"}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/get/apartamentos')
def get_data_mongo_apartamentos():
    try:
        data = str(handler.get_collection("apartamentos"))
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
        handler.insert("lotes", data.to_dict())
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
        handler.insert("apartamentos", data.to_dict())
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/insert_all/lotes', methods=['POST'])
def insert_all_data_mongo_lotes():
    try:
        for doc in list_of_documents_lotes:
            handler.insert("lotes", doc.to_dict())
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mongo/insert_all/apartamentos', methods=['POST'])
def insert_all_data_mongo_apartamentos():
    try:
        for doc in list_of_documents_apartamentos:
            handler.insert("apartamentos", doc.to_dict())
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- AUTENTICAÇÃO --------------------
@app.route('/auth/login', methods=['POST'])
def login():
    try:
        print(handler.get_data("usuarios", "email", "macaco@macaco.com"))

        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"success": False, "message": "Email e senha são obrigatórios"}), 400

        # Usa o método correto com 3 argumentos
        users = handler.get_data(USERS_COLLECTION, "email", email)

        if users and users[0].get("password") == password:
            user = users[0]
            return jsonify({
                "success": True,
                "user": {
                    "name": user.get("name"),
                    "email": user.get("email")
                }
            })

        return jsonify({"success": False, "message": "Usuário ou senha inválidos"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/auth/register', methods=['POST'])
def register():
    try:

        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"success": False, "message": "Nome, email e senha são obrigatórios"}), 400

        existing_user = handler.get_data(USERS_COLLECTION, "email", email)
        if existing_user:
            return jsonify({"success": False, "message": "Email já cadastrado"}), 400

        user_data = {
            "name": name,
            "email": email,
            "password": password
        }

        handler.insert(USERS_COLLECTION, user_data)

        return jsonify({"success": True}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
# -------------------- DASHBOARD --------------------

init_dashboard(app)

# -------------------- MAIN --------------------

if __name__ == '__main__':
    app.run(debug=True)
