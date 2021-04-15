from pyspark.ml import Pipeline
from pyspark.ml.feature import *
from pyspark.ml import Estimator, Transformer
from pyspark.ml.regression import GBTRegressor

tokenizer = Tokenizer(inputCol="reviewText", outputCol="words")
hasher = HashingTF(numFeatures=10000, binary=True, inputCol=tokenizer.getOutputCol(), outputCol="word_vector")
stop_words = StopWordsRemover.loadDefaultStopWords("english")
swr = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol="words_filtered", stopWords=stop_words)
assembler = VectorAssembler(inputCols=[hasher.getOutputCol(), "comment_length"], outputCol="features")
gbt = GBTRegressor(featuresCol=hasher.getOutputCol(), labelCol="overall", stepSize=0.05)

pipeline = Pipeline(stages=[
    tokenizer,
    swr,
    hasher,
    gbt
])