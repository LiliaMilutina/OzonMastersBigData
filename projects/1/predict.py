#!/opt/conda/envs/dsenv/bin/python

import sys, os
import logging
from joblib import load
import pandas as pd
import numpy as np

sys.path.append('.')

from model import model, fields_val

numeric_features = ["if"+str(i) for i in range(1,14)]
list_cat = [4, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 24, 25, 26]
categorical_features = ["cf"+str(i) for i in range(1,27)]

fields_val_ = ["label"] + numeric_features + categorical_features 


# Init the logger
#
logging.basicConfig(level=logging.DEBUG)
logging.info("CURRENT_DIR {}".format(os.getcwd()))
logging.info("SCRIPT CALLED AS {}".format(sys.argv[0]))
logging.info("ARGS {}".format(sys.argv[1:]))

#load the model
model = load("1.joblib")

#read and infere
read_opts=dict(
        sep='\t', names=fields_val_, index_col=False, header=None,
        iterator=True, chunksize=100
)

for df in pd.read_csv(sys.stdin, **read_opts):
    y_pred = model.predict(df)
    out = zip(df.id, y_pred)
    print("\n".join(["{0}\t{1}".format(*i) for i in out]))

