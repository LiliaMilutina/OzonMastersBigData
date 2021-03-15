add file projects/2/predict.py;
add file 2.joblib;

insert into hw2_pred
select transform(*) using '/opt/conda/envs/dsenv/bin/python predict.py' as (id, pred)
from hw2_test 
where if1 is not null and if1 > 20 and if1 < 40;







