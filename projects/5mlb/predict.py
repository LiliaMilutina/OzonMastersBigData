import os, sys
import argparse

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression

import mlflow
import mlflow.sklearn
import mlflow.pyfunc

def parse_args():
    parser = argparse.ArgumentParser(description='example')
    parser.add_argument(
        "--test_path_in",
        type=str
    )
    parser.add_argument(
        "--predict_path_out",
        type=str
    )
    parser.add_argument(
        "--sklearn_model",
        type=str
    )  
    parser.add_argument(
        "--model_version",
        type=int,
        default=0
    )
    return parser.parse_args()

def predict():

    df = pd.read_csv(args.test_path_in)
    
    with mlflow.start_run(args.model_version) as active_run:
        model = mlflow.pyfunc.spark_udf(spark, args.sklearn_model)
        df['y_pred'] = model.predict(df)
     
        result = df[['id', 'pred']]
        result.to_csv(args.predict_path_out, index=False)
        
if __name__ == "__main__":
    train()