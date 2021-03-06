from sklearn import preprocessing
import pandas as pd
import os
from sklearn import ensemble
from sklearn import metrics
import joblib
from . import dispatcher

FOLD = int(os.environ.get("FOLD"))
TRAINING_DATA = os.environ.get("TRAINING_DATA") 
TEST_DATA = os.environ.get("TEST_DATA")
MODEL = os.environ.get("MODEL")

FOLD_MAPPING = {
    0: [1,2,3,4],
    1: [0,2,3,4],
    2: [0,1,3,4],
    3: [0,1,2,4],
    4: [0,1,2,3]
}

if __name__ == '__main__':
    df = pd.read_csv(TRAINING_DATA)
    df_test = pd.read_csv(TEST_DATA)
    train_df = df[df.kfold.isin(FOLD_MAPPING.get(FOLD))]
    valid_df = df[df.kfold == FOLD]

    ytrain = train_df.target.values
    yvalid = valid_df.target.values    

    train_df = train_df.drop(["id", "target", "kfold"], axis = 1)
    valid_df = valid_df.drop(["id","target", "kfold"], axis = 1)


    valid_df  = valid_df[train_df.columns]

    label_encoder = []
    for c in train_df.columns:
        lbl = preprocessing.LabelEncoder()
        lbl.fit(train_df[c].values.tolist()+ valid_df[c].values.tolist() + test_df[c])
        train_df.loc[:,c] = lbl.transform(train_df[c].values.tolist())
        valid_df.loc[:,c] = lbl.transform(valid_df[c].values.tolist())

        label_encoder.append((c, lbl))

    clf = dispatcher.MODELS[MODEL]
    clf.fit(train_df, ytrain)

    preds = clf.predict_proba(valid_df)[:,1]
    print(metrics.roc_auc_score(yvalid, preds))

    joblib.dump(label_encoder, f'models/{MODEL}_{FOLD}_label_encoder.plk')
    joblib.dump(clf, f'models/{MODEL}_{FOLD}.plk')
    joblib.dump(train_df.columns, f'models/{MODEL}_{FOLD}_columns.pkl')