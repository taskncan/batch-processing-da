from flask import Flask, jsonify, send_file
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("API_SECRET_KEY")

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USERNAME')
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
logger.info("Database engine created successfully.")

@app.route('/data', methods=['GET'])
def get_data():
    try:
        logger.info("Fetching data from PostgreSQL table 'aggregated_by_city'.")
        df = pd.read_sql("SELECT * FROM aggregated_by_city", engine)
        
        # Save fetched data as CSV with timestamp in data/processed folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        local_filename = f"data/processed/aggregated_by_city_{timestamp}.csv"
        os.makedirs(os.path.dirname(local_filename), exist_ok=True)
        df.to_csv(local_filename, index=False)
        logger.info("Data saved locally to %s.", local_filename)
        
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        logger.error("Error fetching data: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['GET'])
def download_latest():
    try:
        processed_dir = "data/downloads"
        files = [f for f in os.listdir(processed_dir) if f.startswith("aggregated_by_city") and f.endswith(".csv")]
        if not files:
            logger.error("No CSV file found in %s.", processed_dir)
            return jsonify({"error": "No file found"}), 404
        latest_file = max(files)
        file_path = os.path.join(processed_dir, latest_file)
        logger.info("Sending latest file %s for download.", file_path)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error("Error during file download: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting API service on port 5000.")
    app.run(host="0.0.0.0", port=5000)