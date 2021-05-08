#!/opt/conda/envs/dsenv/bin/python

import os, sys
import argparse

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import log_loss

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

def parse_args():
    parser = argparse.ArgumentParser(description='example')
    parser.add_argument(
        "--train_path",
        type=str
    )
    parser.add_argument(
        "--model_param1",
        type=float,
        default=0.1
    )
    return parser.parse_args()

def main():
        #
    # Model pipeline
    #

    # We create the preprocessing pipelines for both numeric and categorical data.
    numeric_features = ["if"+str(i) for i in range(1,14)]
    categorical_features = ["cf"+str(i) for i in range(1,27)] + ["day_number"]

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    fields = ["id", "label"] + numeric_features + categorical_features
    fields_val = ["id"] + numeric_features + categorical_features

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # Now we have a full prediction pipeline.
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('logregression', LogisticRegression(max_iter=10))
    ])
    
    args = parse_args()

    read_table_opts = dict(sep="\t", names=fields, index_col=False)
    df = pd.read_table(args.train_path, **read_table_opts)

    #split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        df.iloc[:1000,2:], df.iloc[:1000,1], test_size=0.33, random_state=42
    )

    #
    # Train the model
    #
    
    with mlflow.start_run():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        signature = infer_signature(y_train, y_train)
        mlflow.sklearn.log_model(model, "MLmodel", signature=signature)
        model_score = log_loss(y_test, y_pred)
        mlflow.log_metrics({"log_loss": model_score})
        
if __name__ == "__main__":
    main()
