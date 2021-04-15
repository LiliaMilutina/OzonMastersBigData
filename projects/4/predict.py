from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel('WARN')

from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql import functions as f

model_path = sys.argv[0]
data_test_path = sys.argv[1]
result_path = sys.argv[2]

data_test_path = "/datasets/amazon/all_reviews_5_core_test_features.json"
model_path = "/home/users/LiliaMilutina/LiliaMilutina_hw4_output"

pipeline_model = PipelineModel.load(model_path)

schema = StructType([
    StructField("asin", StringType()),
    StructField("id", LongType()),
    StructField("reviewText", StringType()),
    StructField("reviewTime", StringType()),
    StructField("reviewerID", StringType()),
    StructField("reviewerName", StringType()),
    StructField("summary", StringType()),
    StructField("unixReviewTime", LongType()),
    StructField("verified", BooleanType())
])

data_test = spark.read.json(data_test_path, schema=schema, multiLine=True)
data_test.repartition(4).cache()

pred = pipeline_model.transform(data_test)
prediction = pred.select(f.col("prediction").cast("int")).toPandas()
prediction.to_csv(result_path, header=None, index=False)
