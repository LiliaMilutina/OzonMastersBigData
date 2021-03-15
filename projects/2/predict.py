#!/opt/conda/envs/dsenv/bin/python

import sys

import logging
from joblib import load
import pandas as pd
import numpy as np

from model import model, fields_val

#load the model
# model = load("2.joblib")

# read and infere
read_opts=dict(
        sep='\t', names=fields_val, index_col=False, header=None,
        iterator=True, chunksize=1, na_values = '\\N'
)

for df in pd.read_csv(sys.stdin, **read_opts):
#     y_pred = model.predict_proba(df)
#     out = zip(df.id, y_pred[:, 1])
#     print("\n".join(["{0}\t{1}".format(*i) for i in out]))
    print("123\t0")






