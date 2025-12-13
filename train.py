import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import random
import numpy as np
import joblib
from config import FEATURES, TARGET

df = pd.read_csv("data/archive/btc_4h_data_2018_to_2025.csv")
df["prev_close"] = df["Close"].shift(1)
df["open_higher_than_prev_close"] = (df["Open"] > df["prev_close"]).astype(int)
train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]

train.to_csv("data/train.csv", index=False)
test.to_csv("data/test.csv", index=False)

x_train = train[FEATURES]
y_train = train[TARGET]


def goated_model():
    rf = RandomForestClassifier(n_estimators = 100)
    rf.fit(x_train, y_train)
    joblib.dump(rf, "./random_forest.joblib")

goated_model()

