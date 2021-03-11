ADD FILE ./projects/2/model.py
ADD FILE ./projects/2/train.py
ADD FILE ./projects/2/train.sh
ADD FILE ./projects/2/predict.py

INSERT OVERWRITE TABLE hw2_test SELECT * FROM hw2_test WHERE if1 > 20 and if1 < 40;



