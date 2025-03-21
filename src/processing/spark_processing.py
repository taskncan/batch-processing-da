from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USERNAME')
DB_PASS = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

def main():
    spark = SparkSession.builder \
        .appName("YelpDataProcessing") \
        .master("local[*]") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.1") \
        .getOrCreate()

    input_path = "data/raw/yelp_academic_dataset_business.json"
    df = spark.read.json(input_path)

    agg_df = df.groupBy("city").count()

    # Optional: Save aggregated results as JSON
    agg_df.write.mode("overwrite").json("data/processed/aggregated_by_city.json")

    # Write directly from Spark to PostgreSQL with batch
    jdbc_url = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
    agg_df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "aggregated_by_city") \
        .option("user", DB_USER) \
        .option("password", DB_PASS) \
        .option("driver", "org.postgresql.Driver") \
        .option("batchsize", 200) \
        .mode("overwrite") \
        .save()

    spark.stop()

if __name__ == "__main__":
    main()