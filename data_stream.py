import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf


schema = StructType([
    StructField("crime_id", StringType(), True),
    StructField("original_crime_type_name", StringType(), True),
    StructField("report_date", StringType(), True),   
    StructField("call_date", StringType(), True),
    StructField("offense_date", StringType(), True),
    StructField("call_date_time", StringType(), True),
    StructField("call_time", StringType(), True),
    StructField("disposition", StringType(), True),
    StructField("address", StringType(), True),
    StructField("address_type", StringType(), True),
    StructField("agency_id", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("common_location", StringType(), True),
])

def run_spark_job(spark):

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "org.sf.police.service-calls") \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", 200) \
        .option("stopGracefullyOnShutdown", "true") \
        .load()

    df.printSchema()

    kafka_df = df.selectExpr("CAST(value AS STRING)")

    service_table = kafka_df\
        .select(psf.from_json(psf.col('value'), schema).alias("DF"))\
        .select("DF.*")

    distinct_table = service_table \
        .select(psf.col('crime_id'),
                psf.col('original_crime_type_name'),
                psf.col('disposition')).distinct()

    agg_df = distinct_table \
      .groupBy(distinct_table.original_crime_type_name).count()

    query = agg_df \
        .writeStream \
        .trigger(processingTime="10 seconds") \
        .outputMode('complete') \
        .format('console') \
        .start()

    query.awaitTermination()

    radio_code_json_filepath = "./radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)
    
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")
    join_query = agg_df.join(radio_code_df, agg_df.disposition==radio_code_df.disposition, "left_outer")

    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .config("spark.ui.port", 3000) \
        .appName("KafkaSparkStructuredStreaming") \
        .getOrCreate()
    
    spark.conf.set("spark.default.parallelism", "2")
    spark.conf.set("spark.sql.shuffle.partitions", "1")

    run_spark_job(spark)

    spark.stop()
