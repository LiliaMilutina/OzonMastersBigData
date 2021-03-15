#!/opt/conda/envs/dsenv/bin/python

import sys, os
from joblib import load
import pandas as pd
import numpy as np

# We create the preprocessing pipelines for both numeric and categorical data.
numeric_features = ["if"+str(i) for i in range(1,14)]
categorical_features = ["cf"+str(i) for i in range(1,27)] + ["day_number"]
fields_val = ["id"] + numeric_features + categorical_features

# from model import fields_val

# load the model
model = load('2.joblib')

#read and infere
read_opts=dict(
        sep='\t', names=fields_val, index_col=False, header=None,
        iterator=True, chunksize=100, na_values='\\N'
)

for df in pd.read_csv(sys.stdin, **read_opts):
    y_pred = model.predict_proba(df)
    out = zip(df.id, y_pred[:, 1])
    print('\n'.join(['{0}\t{1}'.format(*i) for i in out]))
