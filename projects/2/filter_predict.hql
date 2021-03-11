ADD FILE ./projects/2/model.py;
ADD FILE ./projects/2/train.py;
ADD FILE ./projects/2/train.sh;
ADD FILE ./projects/2/predict.py;

ALTER TABLE hw2_test DROP IF EXISTS PARTITION(if1 < 20 AND if1 < 40);



