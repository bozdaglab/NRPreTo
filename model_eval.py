from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,f1_score,roc_auc_score,precision_score, recall_score
from sklearn.metrics import matthews_corrcoef
import matplotlib.pyplot as plt
import seaborn as sns
import os


def eval_metrics(true,pred,rf_model,dataset_name):

  accuracy = accuracy_score(true,pred)
  precision = precision_score(true,pred,pos_label='positive',average='macro')
  recall = recall_score(true,pred,pos_label='positive',average='macro')
  f1 = f1_score(true,pred,pos_label='positive',average='macro')
  auc = roc_auc_score(true,pred)
  mcc = matthews_corrcoef(true,pred)

  matrix = confusion_matrix(true,pred)

  #creates confusion matrix
  plt.rcParams["figure.figsize"] = (20,8)
  sns.set(font_scale=1.4)
  sns.heatmap(matrix, annot=True, annot_kws={'size':10},
              cmap=plt.cm.Greens, linewidths=0.2,fmt='g')
  plt.xlabel('Predicted label')
  plt.ylabel('True label')

  if os.path.exists('output/confusion_matrix_level_1.png'):
    plt.savefig('output/confusion_matrix_level_2.png')
    plt.close()
  else:
    plt.savefig('output/confusion_matrix_level_1.png')
    plt.close()
  
  #save evaluation metrics of the model to text file
  if os.path.exists('output/' + dataset_name + 'model_evaluation_level_1.txt'):
    output_file = open('output/' + dataset_name + 'model_evaluation_level_2.txt','w')
  else:
    output_file = open('output/' + dataset_name + 'model_evaluation_level_1.txt','w')

  output_file.write("Accuracy: " + str("{:.4f}".format(accuracy)) + "\n")
  output_file.write("Presicion: " + str("{:.4f}".format(precision)) + "\n")
  output_file.write("Recall: " + str("{:.4f}".format(recall)) + "\n")
  output_file.write("F1-macro: " + str("{:.4f}".format(f1)) + "\n")
  output_file.write("AUC score: " + str("{:.4f}".format(auc)) + "\n")
  output_file.write("Matthews Correlation Coefficient: " + str("{:.4f}".format(mcc)) + "\n")

  output_file.close() 

  return None