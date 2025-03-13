from flask import Flask, jsonify
import pandas as pd
from pymongo.synchronous.auth import authenticate

from mongohandler import MongoHandler

handler = MongoHandler('mongodb+srv://filipedaniel2004:LIA123@lia.xqp0e.mongodb.net/?retryWrites=true&w=majority&appName=LIA', 'LIA')
authenticated = False
auth_user = None

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
def get_data_mongo():
    try:
        data = handler.get_collection("lotes")
    except:
        return jsonify({"error": "Error getting data"}), 500
    finally:
        return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)