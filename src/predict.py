from sklearn import preprocessing
import pandas as pd
import os
from sklearn import ensemble
from sklearn import metrics
import joblib
from . import dispatcher


TEST_DATA = os.environ.get("TEST_DATA")
MODEL = os.environ.get("MODEL")

if __name__ == '__main__':
    df = pd.read_csv(TEST_DATA)   


    label_encoder = 
    
    
    
    for FOLD in range(5):
        encoders = joblib.load(os.path.join('models',f'models/{MODEL}_{FOLD}_label_encoder.plk'))
        for c in train_df.columns:
            lbl = preprocessing.LabelEncoder()
            lbl.fit(train_df[c].values.tolist()+ valid_df[c].values.tolist())
            train_df.loc[:,c] = lbl.transform(train_df[c].values.tolist())
            valid_df.loc[:,c] = lbl.transform(valid_df[c].values.tolist())

            label_encoder.append((c, lbl))

        clf = joblib.load(os.path.join('models',f'models/{MODEL}_{FOLD}.plk'))
        columns = joblib.load(os.path.join('models',f'models/{MODEL}_{FOLD}_columns.plk'))

        preds = clf.predict_proba(valid_df)[:,1]
        print(metrics.roc_auc_score(yvalid, preds))

        