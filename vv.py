import pandas as pd
import numpy as np
import sys
import os
import random

import lightgbm as lgb

# Parameters
LABEL_COLUMN_NAME = 'understandingGrade'   # nome da coluna de saida
UNWANTED_COLUMNS = ['filename','nErrors','nErrorsTokens','ntokens','fleshscore',
'avgWordLength','nSpelling','nSpellingTokens','nLongSentence','nStyleErrors',
'nStyleperSent','nvoc','similarityprompt','countDemonstrativo',
'demonstrativoPerSent','countEnclise','enclisePerSent','fstPerson',
'fstPessoaPerSent','countDiscourseMarkers','discourseSent',
'selectinginfoGrade','showknowGrade','solutionGrade','formalGrade','finalGrade']
N_FOLDS = 5

params = {
    "max_bin": 512,
    "max_depth": 50,
    "learning_rate": 0.05,
    "boosting_type": "gbdt",
    "objective": "regression",
    "metric": 'mae',
    "num_leaves": 50,
    "verbose": -1,
    "min_data": 5,
    "boost_from_average": True,
    "random_state": 1
}

def eval_bootstrap(df, features):
    X = df[features]
    y = df[LABEL_COLUMN_NAME].values

    dftrainLGB = lgb.Dataset(data = X, label = y, feature_name = list(X))
    cv_results = lgb.cv(params,
        dftrainLGB,
        num_boost_round=100,
        nfold=N_FOLDS,
        metrics='mae',
        early_stopping_rounds=25,
        shuffle=True,
        stratified=False
    )
    return(cv_results['l1-mean'][-1])


# Reads dataset
df = pd.read_csv(sys.argv[1])
df.dropna(axis=0, subset=[LABEL_COLUMN_NAME], inplace=True)

all_features = list(df.columns)

for f in UNWANTED_COLUMNS + [LABEL_COLUMN_NAME]:
    all_features.remove(f)

f = []
i = 0
for f1 in all_features:
    if i == 50: break
    if f1 in f: continue
    k = 1000
    x = f1
    i = i + 1
    j = 0
    for f2 in all_features:
         if f2 in f: continue
         j = j + 1
         f.insert(len(f), f2)
         A = eval_bootstrap(df, f)
         print("%s,%f" % (f,A))
         z = A
         f.remove(f2)
         sys.stdout.flush()
         if z < k:
             x = f2
             k = z
    f.insert(len(f), x)
