from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("API_SECRET_KEY")

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USERNAME')
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

@app.route('/data', methods=['GET'])
def get_data():
    try:
        df = pd.read_sql("SELECT * FROM aggregated_by_city", engine)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)