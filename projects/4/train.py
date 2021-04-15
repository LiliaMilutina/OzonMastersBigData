import os
import sys
import random

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel('WARN')

from model import pipeline
from pyspark.sql.types import *


data_train_path = sys.argv[0]
model_path = sys.argv[1]

schema = StructType([
    StructField("asin", StringType()),
    StructField("id", LongType()),
    StructField("overall", FloatType()),
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

pipeline_model = pipeline.fit(data_train)

pipeline_model.write().overwrite().save(model_path)