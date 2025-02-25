from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/data')
def get_data():
    df = pd.DataFrame({'Nome': ['Alice', 'Bob'], 'Idade': [25, 30]})
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)