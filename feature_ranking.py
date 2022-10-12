from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def feature_rank(df):

  #assign features as X and label as y 
  X = df.drop(['nuclear_receptor'],axis=1).values
  y = df['nuclear_receptor'].values

  #initialize Random Forest clasifier
  clf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
  clf.fit(X, y)

  feature_selector = BorutaPy(clf, n_estimators='auto', verbose=2, random_state=1)
  feature_selector.fit(X, y)

  #get a tuple of (feature name, rank, Importance = True or False)
  feature_ranks = list(zip(df.columns,feature_selector.ranking_,feature_selector.support_))
  selected_feat = []

  #loop through feature_ranks and select only those features with True support
  for item in feature_ranks:
    if item[2] == True:
      selected_feat.append(item[0])
  selected_feat.append('nuclear_receptor')
  
  return selected_feat
