from pyspark.sql import SparkSession
import os
from sqlalchemy import create_engine

def main():
    spark = SparkSession.builder \
        .appName("YelpDataProcessing") \
        .master("local[*]") \
        .getOrCreate()

    input_path = "data/raw/yelp_academic_dataset_business.json"
    df = spark.read.json(input_path)
    agg_df = df.groupBy("city").count()
    agg_df.write.json("data/processed/aggregated_by_city.json")

    postgres_url = f"postgresql+psycopg2://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:5432/yelpdb"
    engine = create_engine(postgres_url)
    agg_pd = agg_df.toPandas()
    agg_pd.to_sql("aggregated_by_city", engine, if_exists="replace", index=False)

    spark.stop()

if __name__ == "__main__":
    main()