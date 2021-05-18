#!/opt/conda/envs/dsenv/bin/python

import os, sys
import argparse
from etl import etl
from train import train 

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
        
if __name__ == "__main__":
    etl()
    train()
