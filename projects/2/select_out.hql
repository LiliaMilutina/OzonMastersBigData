INSERT OVERWRITE DIRECTORY 'LiliaMilutina_hiveout' ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' SELECT * FROM hw2_pred;
