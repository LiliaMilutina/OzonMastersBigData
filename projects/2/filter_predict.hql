ADD FILE ./projects/2/model.py;
ADD FILE ./projects/2/predict.py;
ADD FILE 2.joblib;

FROM (
FROM hw2_test
SELECT * WHERE if1 is not null and if1 > 20 and if1 < 40) hw_filter
INSERT OVERWRITE TABLE hw2_pred
SELECT TRANSFORM (hw_filter.*)
USING 'predict.py'
AS id, pred;







