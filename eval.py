import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from config import FEATURES, TARGET

test = pd.read_csv("data/test.csv")

x_test = test[FEATURES]
y_test = test[TARGET]

rf = joblib.load("./random_forest.joblib")
y_pred = rf.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", classification_rep)