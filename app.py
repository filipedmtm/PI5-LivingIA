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
    handler.connect() #Está dando error.

if __name__ == '__main__':
    app.run(debug=True)