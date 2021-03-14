ADD FILE ./projects/2/model.py;
ADD FILE ./projects/2/predict.py;

from hw2_test select transform (*) USING '/opt/conda/envs/dsenv/bin/python ./projects/2/predict.py';







