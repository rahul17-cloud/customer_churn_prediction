import pandas as pd
import numpy as np

def clean_data(df):
    df = df.dropna()
    if 'Month' not in df.columns:

        base_date = pd.to_datetime("2020-01-01")
        months = pd.date_range(start=base_date, periods=min(len(df), 120), freq='MS')
        repeated_months = np.resize(months.strftime('%b'), len(df))
        df['Month'] = repeated_months

    
    if 'Sales' not in df.columns:
        df['Sales'] = np.random.randint(500, 1500, size=len(df))

    return df
