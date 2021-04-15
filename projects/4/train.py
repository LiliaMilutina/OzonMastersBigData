import os
import sys
import random

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

from model import pipeline
from pyspark.sql.types import *


data_train_path = sys.argv[0]
model_path = sys.argv[1]

data_train_path = "/datasets/amazon/all_reviews_5_core_train.json"
model_path = "/home/users/LiliaMilutina/LiliaMilutina_hw4_output"


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

import subprocess
cat = subprocess.Popen(["hdfs", "dfs", "-mkdir", model_path], stdout=subprocess.PIPE)

pipeline_model.write().overwrite().save(model_path)
