CREATE TABLE LiliaMilutina_checker.hw2_pred (
    id INT,
    pred FLOAT)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
    LINES TERMINATED BY '\n'
    STORED AS TEXTFILE
    LOCATION 'LiliaMilutina_hw2_pred';
