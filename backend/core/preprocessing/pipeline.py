import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from typing import Dict

class PreprocessingPipeline:
    def transform(self, df: pd.DataFrame, config: Dict) -> pd.DataFrame:
        df = df.copy()

        # Missing value handling
        if 'handle_missing' in config:
            strategy = config['handle_missing'].get('strategy', 'mean')
            columns = config['handle_missing'].get('columns', df.columns)
            missing_cols = set(columns) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Missing columns: {missing_cols}")
            
            numeric_cols = df[columns].select_dtypes(include=np.number).columns
            if strategy == 'drop':
                df = df.dropna(subset=numeric_cols)
            else:
                imputer = SimpleImputer(strategy=strategy)
                df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

        # Categorical encoding
        if 'encode_categorical' in config:
            columns = config['encode_categorical'].get('columns', [])
            if columns:
                missing_cat = set(columns) - set(df.columns)
                if missing_cat:
                    raise ValueError(f"Categorical columns not found: {missing_cat}")
                
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                encoded_data = encoder.fit_transform(df[columns])
                encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(columns))
                df = pd.concat([df.drop(columns, axis=1), encoded_df], axis=1)

        # Feature scaling
        if 'scale_features' in config:
            columns = config['scale_features'].get('columns', [])
            if columns:
                missing_scale = set(columns) - set(df.columns)
                if missing_scale:
                    raise ValueError(f"Scaling columns not found: {missing_scale}")
                
                scaler = StandardScaler()
                df[columns] = scaler.fit_transform(df[columns])

        return df
