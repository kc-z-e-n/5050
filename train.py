import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import random
import numpy as np

SEED = 50
random.seed(SEED)
np.random.seed(SEED)

df = pd.read_csv("data/archive/btc_4h_data_2018_to_2025.csv")
df["prev_close"] = df["Close"].shift(1)
df["open_higher_than_prev_close"] = (df["Open"] > df["prev_close"]).astype(int)
train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]

def goated_model():
    return random.randint(0, 1)

def eval():
    count = 0
    for row in test.itertuples(index=False):
        if row[-1] == goated_model():
            count += 1
    return count / len(test)

print(eval())