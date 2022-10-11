import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import sys
sys.path.append('/content/drive/MyDrive/Sirisha_model_check/GItHub') #for test only
from feature_ranking import *
from hyperparameter_tune import *
from utilities import *
from model_eval import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--feature_selection', type=int, required=False, default= 1)
parser.add_argument('--hyperparameter_tune', type=int, required=False, default= 1)
args = parser.parse_args()

#read train,independent,hprd and refseq dataset
train = '/content/drive/MyDrive/Sirisha_model_check/GItHub/Data/subset_of_lvl1_train_dataset.csv'
indep = '/content/drive/MyDrive/Sirisha_model_check/GItHub/Data/subset_of_lvl1_independent_dataset.csv'
hprd = '/content/drive/MyDrive/Sirisha_model_check/GItHub/Data/subset_of_HPRD_dataset.csv'
refseq = '/content/drive/MyDrive/Sirisha_model_check/GItHub/Data/subset_of_Refseq_dataset.csv'

#combine train and indep dataset to train model
combined_df = combined_data(train,indep)

#apply label map to convert all NR sub-class to 1 and Non-NR to 0
hprd_df = HPRD_Refseq_label_map_level_1(hprd)
refseq_df = HPRD_Refseq_label_map_level_1(refseq)

if args.feature_selection == 1:
  #rank most important feature using Borutapy feature selection method
  #this fundtion return the list of important features
  selected_feat = feature_rank(combined_df)

  #create a subset of Combined, HPRD and Refseq dataset containg only important features
  combined_imp_feat_df = combined_df[np.intersect1d(combined_df.columns, selected_feat)]
  hprd_imp_feat_df = hprd_df[np.intersect1d(hprd_df.columns, selected_feat)]
  refseq_imp_feat_df = refseq_df[np.intersect1d(refseq_df.columns, selected_feat)]

else:
  combined_imp_feat_df = combined_df
  hprd_imp_feat_df = hprd_df
  refseq_imp_feat_df = refseq_df


X = combined_imp_feat_df.drop(['nuclear_receptor'],axis=1).values
y = combined_imp_feat_df['nuclear_receptor'].values

if args.hyperparameter_tune == 1:
  #if user have choosen to perform hyper parameter tuning, then hyperparameters of Random Forest model will be tuned using Hyperopt python package
  tuned_RF_model = hyperparameter_tune(X,y).fit(X,y)

  #test tuned RF model on HPRD dataset
  eval_metrics(hprd_imp_feat_df['nuclear_receptor'].values,
               base_RF_model.predict(hprd_imp_feat_df.drop(['nuclear_receptor'],axis=1).values),
               base_RF_model)

  #test tuned RF model on Refseq dataset
  eval_metrics(refseq_imp_feat_df['nuclear_receptor'].values,
               base_RF_model.predict(refseq_imp_feat_df.drop(['nuclear_receptor'],axis=1).values),
               base_RF_model)
  
else:
  #if user have not choose to perform hyper parameter tuning, then base Random Forest model will be trained
  base_RF_model = RandomForestClassifier()
  base_RF_model.fit(X, y)

  #test base RF model on HPRD
  eval_metrics(hprd_imp_feat_df['nuclear_receptor'].values,
               base_RF_model.predict(hprd_imp_feat_df.drop(['nuclear_receptor'],axis=1).values),
               base_RF_model)

  #test base RF model on Refseq dataset
  eval_metrics(refseq_imp_feat_df['nuclear_receptor'].values,
               base_RF_model.predict(refseq_imp_feat_df.drop(['nuclear_receptor'],axis=1).values),
               base_RF_model)