import os, sys
import argparse

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import log_loss

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
import mlflow
import mlflow.sklearn

def parse_args():
    parser = argparse.ArgumentParser(description='example')
    parser.add_argument(
        "--train_path_in",
        type=str
    )
    parser.add_argument(
        "--sklearn_model",
        type=str
    )
    parser.add_argument(
        "--model_param1",
        type=int,
        default=10
    )
    return parser.parse_args()

def train():
    
    args = parse_args()

    data_train = pd.read_parquet(args.train_path_in)
    
    with mlflow.start_run():
        model.fit(data_train.iloc[:1000, :])
        
        #log model params
        mlflow.log_param("model_param1", args.model_param1)
        mlflow.sklearn.log_model(model, artifact_path=args.sklearn_model)
        
if __name__ == "__main__":
    train()