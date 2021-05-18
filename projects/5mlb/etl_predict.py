#!/opt/conda/envs/dsenv/bin/python

import os, sys
import argparse
from etl import etl
from predict import predict

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
    return parser.parse_args()
        
if __name__ == "__main__":
    etl()
    predict()
