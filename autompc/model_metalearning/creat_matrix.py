import os, glob
import pickle
import numpy as np
import pandas as pd

from autompc.sysid.autoselect import AutoSelectModel
from autompc.tuning.model_evaluator import CrossValidationModelEvaluator, HoldoutModelEvaluator, ModelEvaluator
from autompc.model_metalearning.meta_utils import load_data, load_cfg, meta_data


data_path = '/home/baoyul2/autompc/autompc/model_metalearning/meta_data'
cfg_path = '/home/baoyul2/autompc/autompc/model_metalearning/meta_cfg'
matrix_path = '/home/baoyul2/autompc/autompc/model_metalearning/meta_matrix'
matrix_row_path = '/home/baoyul2/autompc/autompc/model_metalearning/meta_matrix_row'

def create_matrix(names, data_path=data_path, cfg_path=cfg_path, matrix_path=matrix_path,
                  eval_metric='rmse', eval_horizon=1, eval_quantile=None, eval_folds=3):
    
    output_results_dictionary = {}
    # data
    for data_name in names:
        print(data_name)
        system, trajs = load_data(data_path, data_name)
        scores = []
        # config
        for cfg_name in names:
            cfg = load_cfg(cfg_path, cfg_name)
            print(cfg)
            model = AutoSelectModel(system)
            model.set_config(cfg)
            evaluator = CrossValidationModelEvaluator(trajs, eval_metric, horizon=eval_horizon, quantile=eval_quantile, num_folds=eval_folds,
                        rng=np.random.default_rng(100))
            score = evaluator(model)
            scores.append(score)
        output_results_dictionary[data_name] = scores
    
    matrix = pd.DataFrame(data=output_results_dictionary)
    matrix = matrix.transpose()
    
    # save matrix
    output_file_name = os.path.join(matrix_path, 'matrix_big.pkl')
    print("Dumping to ", output_file_name)
    with open(output_file_name, 'wb') as fh:
        pickle.dump(matrix, fh)
    
    return matrix

# def create_matrix(data_name, names=meta_data, data_path=data_path, cfg_path=cfg_path, matrix_path=matrix_path,
#                   eval_metric='rmse', eval_horizon=1, eval_quantile=None, eval_folds=3):
    
#     output_results_dictionary = {}
#     # data
#     print("============Start Job {}============".format(data_name))
#     # print(data_name)
#     system, trajs = load_data(data_path, data_name)
#     scores = []
#     # config
#     for cfg_name in names:
#         cfg = load_cfg(cfg_path, cfg_name)
#         # print(cfg)
#         model = AutoSelectModel(system)
#         model.set_config(cfg)
#         evaluator = CrossValidationModelEvaluator(trajs, eval_metric, horizon=eval_horizon, quantile=eval_quantile, num_folds=eval_folds,
#                     rng=np.random.default_rng(100))
#         score = evaluator(model)
#         scores.append(score)
#     output_results_dictionary[data_name] = scores
    
#     # matrix = pd.DataFrame(data=output_results_dictionary)
#     # matrix = matrix.transpose()
    
#     # # save matrix
#     # output_file_name = os.path.join(matrix_path, 'matrix.pkl')
#     # print("Dumping to ", output_file_name)
#     # with open(output_file_name, 'wb') as fh:
#     #     pickle.dump(matrix, fh)

#     # save result
#     output_file_name = os.path.join(matrix_row_path, data_name+'_row.pkl')
#     print("Dumping to ", output_file_name)
#     with open(output_file_name, 'wb') as fh:
#         pickle.dump(output_results_dictionary, fh)
    
#     print("============End Job {}============".format(data_name))
    
#     return output_results_dictionary

if __name__ == "__main__":
    matrix = create_matrix(meta_data)
    print(matrix)