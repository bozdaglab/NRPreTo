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

#evaluation metrics
#takes list of true label, list of predicted label and model that is used to predict labels
#returns evaluation score and saves confusion matrix to output directory
def eval_metrics(true,pred,rf_model):

  accuracy = accuracy_score(true,pred)
  precision = precision_score(true,pred,pos_label='positive',average='macro')
  recall = recall_score(true,pred,pos_label='positive',average='macro')
  f1 = f1_score(true,pred,pos_label='positive',average='macro')
  roc = roc_auc_score(true, rf_model.predict_proba(true),average='macro',multi_class='ovr')
  mcc = matthews_corrcoef(true,pred)

  matrix = confusion_matrix(true,pred)

  plt.rcParams["figure.figsize"] = (20,8)
  sns.set(font_scale=1.4)
  sns.heatmap(matrix, annot=True, annot_kws={'size':10},
              cmap=plt.cm.Greens, linewidths=0.2,fmt='g')
  plt.xlabel('Predicted label')
  plt.ylabel('True label')

  plt.savefig('confusion_matrix.png')

  return accuracy,precision,recall,f1,roc,mcc