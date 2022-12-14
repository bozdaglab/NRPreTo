from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,f1_score,roc_auc_score,precision_score, recall_score
from sklearn.metrics import matthews_corrcoef
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#takes train and independent dataset and returns combination of them
def combined_data(train,indep):
  train_df = pd.read_csv(train,index_col=0)
  train_df = train_df.drop(['protein_name'],axis=1)

  indep_df = pd.read_csv(indep,index_col=0)
  indep_df = indep_df.drop(['protein_name'],axis=1)
  indep_df = indep_df.dropna(axis=0)

  combined_df = [train_df,indep_df]
  comb_train = pd.concat(combined_df)

  return comb_train 

#label mapping of HPRD and refseq dataset for level 1 model
#takes HPRD or Refseq dataset and returns dataset with newly mapped label
def HPRD_Refseq_label_map_level_1(external_dataset):
  #label dictionary of NRs sub-class and NonNRs
  label_map = {0: 1,1 : 1,2 : 1,3 : 1,4 : 1,5 : 1,6 : 1,'6' : 1,'NonNR' : 0}

  external_dataset_df = pd.read_csv(external_dataset,index_col=0)
  external_dataset_df = external_dataset_df.drop(['protein_name'],axis=1)

  #apply label dictionary to convert all NR sub-class to 1 and Non-NR to 0
  external_dataset_df['nuclear_receptor'] = external_dataset_df['nuclear_receptor'].apply( lambda x : label_map[x])

  return external_dataset_df

#label mapping of combined dataset for level 2 model
#takes combined dataset and returns dataset with newly mapped label
def Combined_dataset_label_map_level_2(combined_dataset):
  #label dictionary of NRs sub-class (0-6)
  label_map = {'NR1_thyroid_hormone_like':1, 'NR2_HNF4_like':2, 'NR3_estrogen_like':3,
       'NR4_nerve_growth_factor_IB-like':4, 'NR5_fushi_tarazu-F1_like':5,
       'NR6_germ_cell_nuclear_factor_like':6, 'NR0_knirps_and_DAX_like':0}

  #apply label dictionary to convert all NR sub-class to 1 and Non-NR to 0
  combined_dataset['nuclear_receptor'] = combined_dataset['nuclear_receptor'].apply( lambda x : label_map[x])

  return combined_dataset

#train and test spli
#takes dataset and returns test and train set
def train_test_split(dataset):

  X = dataset.drop(['nuclear_receptor'],axis=1).values
  y = dataset['nuclear_receptor'].values

  return train_test_split(X, y, test_size = 0.3,stratify=y)

#get index of HPRD and refseq dataset in order to filter True Positive prediction only
#takes external dataset and predicted label of external dataset
#return external dataset will True Positive label only
def select_true_positive_only(external_dataset,external_dataset_pred):
  dataset_index = external_dataset['nuclear_receptor']
  #zip true, pred label with index and select only true positive
  pred_idx = list(zip(dataset_index.index.tolist(),dataset_index.tolist() ,external_dataset_pred.tolist()))
  true_positive_idx = [idx for idx,true,pred in pred_idx if pred!=0 and true==pred]
  #select data points with True Positive prediction only
  true_positive_label_only = external_dataset.loc[true_positive_idx]

  return true_positive_label_only