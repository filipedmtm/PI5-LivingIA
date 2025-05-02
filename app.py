from flask import Flask, jsonify
import pandas as pd
from mongohandler import MongoHandler

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

#@app.route('/mongo/load/apartamentos')
#app.route('/mongo/load/lotes')

if __name__ == '__main__':
    app.run(debug=True)