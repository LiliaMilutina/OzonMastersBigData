ADD FILE ./projects/2/model.py;
ADD FILE ./projects/2/predict.py;
ADD FILE ./2.joblib;

insert into hw2_pred select transform(*) using 'predict.py' as (id, pred) from hw2_test where if1 is not null and if1 > 20 and if1 < 40;







