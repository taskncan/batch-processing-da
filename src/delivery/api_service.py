from flask import Flask, jsonify
import os
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("API_SECRET_KEY")

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("POSTGRES_HOST", "postgres")
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/yelpdb")

@app.route('/data', methods=['GET'])
def get_data():
    try:
        df = pd.read_sql("SELECT * FROM aggregated_by_city", engine)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)