from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def feature_rank(df):

  #assign features as X and label as y 
  X = df.drop(['nuclear_receptor'],axis=1)
  y = df['nuclear_receptor']

  #initialize Random Forest clasifier
  clf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
  clf.fit(X, y)

  feature_selector = BorutaPy(clf, n_estimators='auto', verbose=2, random_state=1)
  feature_selector.fit(X, y)

  feature_ranks = list(zip(df.columns,feature_selector.ranking_,feature_selector.support_))

  selected_feat_df = pd.DataFrame(feature_ranks,columns =['Feature','Ranking','Important?'])

  return selected_feat_df
