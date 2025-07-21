import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os
import sys


if len(sys.argv) > 1:
    csv_file = sys.argv[1]
else:
    csv_file = 'sample.csv'

df = pd.read_csv(csv_file)


target_candidates = [col for col in df.columns if col.lower() == 'churn']
if not target_candidates:
    raise ValueError("No target column named 'Churn' found in the CSV file.")
target_col = target_candidates[0]


feature_cols = [col for col in df.columns if col != target_col]

X = df[feature_cols].copy()
y = df[target_col]


for col in X.select_dtypes(include='object').columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])


if y.dtype == 'object':
    le_target = LabelEncoder()
    y = le_target.fit_transform(y)

    print(f"Target mapping: {dict(zip(le_target.classes_, le_target.transform(le_target.classes_)))}")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)


model_dir = os.path.dirname(__file__)
model_path = os.path.join(model_dir, 'churn_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)


accuracy = model.score(X_test, y_test)
print(f"Model trained and saved to {model_path}")
print(f"Features used: {feature_cols}")
print(f"Validation accuracy: {accuracy:.4f}")