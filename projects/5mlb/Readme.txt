name: My Project

conda_env: conda.yaml

entry_points:
  predict:
    parameters:
      test_path_in: {type: string}
      predict_path_out: {type: string}
      sklearn_model: {type: string}
      model_version: {type: int, default: 0}
    command: |
      python predict.py \
      --test_path_in={test_path_in} \
      --predict_path_out={predict_path_out} \
      --sklearn_model={sklearn_model} \
      --model_version={model_version}
  train:
    parameters:
      train_path_in: {type: string}
      sklearn_model: {type: string}
      model_param1: {type: int, default: 10}
    command: |
      python train.py \
      --train_path_in={train_path_in} \
      --sklearn_model={sklearn_model} \
      --model_param1={model_param1}
  etl:
    parameters:
      train_path_in_raw: {type: string}
      train_path_in: {type: string}
    command: |
      python train.py \
      --train_path_in_raw={train_path_in_raw} \
      --train_path_in={train_path_in}
  main:
    parameters:
      train_path_in: {type: string}
      sklearn_model: {type: string}
      model_param1: {type: int, default: 10}
    command: |
      python main.py \
      --train_path_in={train_path_in} \
      --sklearn_model={sklearn_model} \
      --model_param1={model_param1}
  etl_predict:
    parameters:
      test_path_in: {type: string}
      predict_path_out: {type: string}
      sklearn_model: {type: string}
      model_version: {type: int, default: 0}
    command: |
      python etl_predict.py \
      --test_path_in={test_path_in} \
      --predict_path_out={predict_path_out} \
      --sklearn_model={sklearn_model} \
      --model_version={model_version}