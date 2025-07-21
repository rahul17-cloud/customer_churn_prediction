import os
import pickle
import pandas as pd

def load_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'churn_model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def predict_churn(model, df):
    
    if hasattr(model, 'feature_names_in_'):
        feature_cols = list(model.feature_names_in_)
    else:
        
        feature_cols = [col for col in df.columns if col.lower() != 'churn']

    missing = [col for col in feature_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in uploaded file: {', '.join(missing)}")

    X = df[feature_cols].copy()

    
    for col in X.select_dtypes(include='object').columns:
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])

    preds = model.predict(X)
    return pd.Series(preds)