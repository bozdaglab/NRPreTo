from feature_ranking import *
from hyperparameter_tune import *
from utilities import *
from model_eval import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import sys
sys.path.append('/content/drive/MyDrive/Sirisha_model_check/GItHub') #for test only
from feature_ranking import *
from hyperparameter_tune import *
from utilities import *
from model_eval import *

def RF_model(a,b,combined_df,hprd_df,refseq_df):
  if a == 1:
    #rank most important feature using Borutapy feature selection method
    #this function return the list of important features
    selected_feat = feature_rank(combined_df)
    #create a subset of Combined, HPRD and Refseq dataset containg only important features
    combined_imp_feat_df = combined_df[np.intersect1d(combined_df.columns, selected_feat)]
    hprd_imp_feat_df = hprd_df[np.intersect1d(hprd_df.columns, selected_feat)]
    refseq_imp_feat_df = refseq_df[np.intersect1d(refseq_df.columns, selected_feat)]

  else:
    #if user have choosen not to perform feature selection, then all features will be used for model training
    combined_imp_feat_df = combined_df
    hprd_imp_feat_df = hprd_df
    refseq_imp_feat_df = refseq_df

  X = combined_imp_feat_df.drop(['nuclear_receptor'],axis=1).values
  y = combined_imp_feat_df['nuclear_receptor'].values

  #if user have choosen to perform hyper parameter tuning, then hyperparameters of Random Forest model will be tuned using Hyperopt python package
  #if args.hyperparameter_tune == 1:
  hprd_pred = []
  refseq_pred = []

  if b == 1:

    tuned_RF_model = hyperparameter_tune(X,y).fit(X,y)
    #predict HPRD label using base RF model
    hprd_tuned_model_pred = tuned_RF_model.predict(hprd_imp_feat_df.drop(['nuclear_receptor'],axis=1).values)
    refseq_tuned_model_pred = tuned_RF_model.predict(refseq_imp_feat_df.drop(['nuclear_receptor'],axis=1).values)

    #get tuned model evaluation on HPRD and Refseq dataset
    eval_metrics(hprd_imp_feat_df['nuclear_receptor'].values,hprd_tuned_model_pred, tuned_RF_model)
    eval_metrics(refseq_imp_feat_df['nuclear_receptor'].values,refseq_tuned_model_pred,tuned_RF_model)
    
    hprd_pred = hprd_tuned_model_pred
    refseq_pred = refseq_tuned_model_pred   
    
  else:
    #if user have not choose to perform hyper parameter tuning, then Random Forest model with default hyperparameters will be trained
    base_RF_model = RandomForestClassifier()
    base_RF_model.fit(X, y)
    #predict HPRD label using base RF model
    hprd_base_model_pred = base_RF_model.predict(hprd_imp_feat_df.drop(['nuclear_receptor'],axis=1).values)
    refseq_base_model_pred = base_RF_model.predict(refseq_imp_feat_df.drop(['nuclear_receptor'],axis=1).values)

    #get base model evaluation on HPRD and Refseq dataset
    eval_metrics(hprd_imp_feat_df['nuclear_receptor'].values,hprd_base_model_pred,base_RF_model)
    eval_metrics(refseq_imp_feat_df['nuclear_receptor'].values,refseq_base_model_pred,base_RF_model)

    hprd_pred = hprd_tuned_model_pred
    refseq_pred = refseq_tuned_model_pred 
  
  return hprd_pred, refseq_pred