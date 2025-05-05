from flask import Flask, jsonify
import pandas as pd
from mongohandler import MongoHandler
from document import document
from documents_list import list_of_documents

handler = MongoHandler('mongodb+srv://filipedaniel2004:LIA123@lia.xqp0e.mongodb.net/', 'living_datas')

app = Flask(__name__)

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

@app.route('/mongo/insert/lotes')
def insert_data_mongo_lotes():
    try:
        data = document(
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

@app.route('/mongo/insert/apartamentos')
def insert_data_mongo_apartamentos():
    try:
        data = document(
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

@app.route('/mongo/insert_all/lotes')
def insert_all_data_mongo_lotes():
    try:
        for i in range(len(list_of_documents)):
            data = list_of_documents[i].to_dict()
            handler.insert("lotes", data)

        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)