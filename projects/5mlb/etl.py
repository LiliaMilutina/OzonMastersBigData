#!/opt/conda/envs/dsenv/bin/python

import os, sys
import argparse

import random

def parse_args():
    parser = argparse.ArgumentParser(description='example')
    parser.add_argument(
        "--train_path_in_raw",
        type=str
    )
    parser.add_argument(
        "--train_path_in",
        type=str
    )
    return parser.parse_args()

def etl():
    SPARK_HOME = "/usr/hdp/current/spark2-client"
    PYSPARK_PYTHON = "/opt/conda/envs/dsenv/bin/python"
    os.environ["PYSPARK_PYTHON"]= PYSPARK_PYTHON
    os.environ["SPARK_HOME"] = SPARK_HOME

    PYSPARK_HOME = os.path.join(SPARK_HOME, "python/lib")
    sys.path.insert(0, os.path.join(PYSPARK_HOME, "py4j-0.10.7-src.zip"))
    sys.path.insert(0, os.path.join(PYSPARK_HOME, "pyspark.zip"))

    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    data_train_path = args.train_path_in_raw
    data_train_ready = args.train_path_in

    schema = StructType([
        StructField("asin", StringType()),
        StructField("id", LongType()),
        StructField("label", IntegerType()),
        StructField("reviewText", StringType()),
        StructField("reviewTime", StringType()),
        StructField("reviewerID", StringType()),
        StructField("reviewerName", StringType()),
        StructField("summary", StringType()),
        StructField("unixReviewTime", LongType()),
        StructField("verified", BooleanType()),
    ])

    data_train = spark.read.json(data_train_path, schema=schema, multiLine=True)
    data_train.repartition(4).cache()

    data_train.write.mode('overwrite').parquet(data_train_ready)
        
if __name__ == "__main__":
    etl()
