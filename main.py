import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import sys
sys.path.append('/content/drive/MyDrive/Sirisha_model_check/GItHub') #for test only

from RF_model import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--feature_selection', type=int, required=False, default= 1)
parser.add_argument('--hyperparameter_tune', type=int, required=False, default= 1)
args = parser.parse_args()


#read train,independent,hprd and refseq dataset
train_lvl1 = 'Data/subset_of_lvl1_train_dataset.csv'
indep_lvl1 = 'Data/subset_of_lvl1_independent_dataset.csv'
train_lvl2 = 'Data/subset_of_lvl2_train_dataset.csv'
indep_lvl2 = 'Data/subset_of_lvl2_independent_dataset.csv'

hprd = 'Data/subset_of_HPRD_dataset.csv'
refseq = 'Data/subset_of_Refseq_dataset.csv'

#combine train and indep dataset to train level-1 model
combined_level1_df = combined_data(train_lvl1,indep_lvl1)

#apply label map to convert all NR sub-class to 1 and Non-NR to 0
hprd_df = HPRD_Refseq_label_map_level_1(hprd)
refseq_df = HPRD_Refseq_label_map_level_1(refseq)

#-------------------LEVEL-1 Model (NR vs NRs prediction)------------------------
#if user have choosen to perform feature selection, then importtant features will be selected using Borutapy python package
#if user have choosen not to perform feature selection, then all features will be used for model training
#if user have choosen to perform hyper parameter tuning, then hyperparameters of Random Forest model will be tuned using Hyperopt python package
#if user have not choose to perform hyper parameter tuning, then Random Forest model with default hyperparameters will be trained

#train RF model using combined dataset and test on HPRD and Refseq dataset
#following level will also returns list of predicted label for HPRD and refseq dataset
#evaluation results(confusion matrix and result table) will be saved inside 'Output' folder
print('Training and Testing Level-1 RF model')
hprd_pred_level_1,refseq_pred_level_1 = RF_model(args.feature_selection,args.hyperparameter_tune,combined_level1_df,hprd_df,refseq_df)

#-------------------LEVEL-2 Model (sub-NRs (NR0,NR1,NR2,NR3,NR4,NR5 and NR6) prediction)------------------------
#combine train and indep dataset to train level-1 model
combined_level2_df = combined_data(train_lvl2,indep_lvl2)

#apply label map to convert all NR sub-class to 0-6
combined_level2_df = Combined_dataset_label_map_level_2(combined_level2_df)

#reread HPRD and Refseq dataset without label mapping
hprd_df = pd.read_csv(hprd,index_col=0)
refseq_df = pd.read_csv(refseq,index_col=0)

#get index of HPRD and refseq dataset in order to filter True Positive prediction only
hprd_TP_only = select_true_positive_only(hprd_df,hprd_pred_level_1)
refseq_TP_only = select_true_positive_only(refseq_df,refseq_pred_level_1)

#train RF model using combined dataset and test on HPRD and Refseq dataset
#following level will also returns list of predicted label for HPRD and refseq dataset
#evaluation results(confusion matrix and result table) will be saved inside 'Output' folder
print('Training and Testing Level-2 RF model')
if hprd_TP_only.shape[1] or refseq_TP_only.shape[1] == 0:
  print('Cannot proceed to level 2 predict as level 1 model did not predited any True Positive. Try feature selection and Hyperparameters tuning.')
else:
  RF_model(args.feature_selection,args.hyperparameter_tune,combined_level1_df,combined_level2_df,hprd_TP_only,refseq_TP_only)
print('Complete !!!')