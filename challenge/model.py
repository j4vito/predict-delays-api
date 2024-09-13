import pandas as pd
from typing import Tuple, Union, List
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import xgboost as xgb
import numpy as np
from datetime import datetime

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.
        self.features_cols = [
        "OPERA_Latin American Wings", 
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air"
    ]
        self.fitted = False
        self.valid_columns = []

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ):
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        train_columns = ['OPERA', 'MES', 'TIPOVUELO']
        if target_column is not None:
            train_columns.append(target_column)
            data['min_diff'] = data.apply(get_min_diff, axis = 1)
            threshold_in_minutes = 15
            data[target_column] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)

        
        training_data = shuffle(data[train_columns], random_state = 111)
        features = pd.concat([
        pd.get_dummies(training_data['OPERA'], prefix = 'OPERA'),
        pd.get_dummies(training_data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
        pd.get_dummies(training_data['MES'], prefix = 'MES')], 
        axis = 1
        )
        #if any column of features is not in self.valid_columns, return None
        for col in features.columns:
            if (col not in self.valid_columns) and self.fitted:
                print(f"{col} not in {self.valid_columns}")
                return None
        
        for col in self.features_cols:
            if col not in features.columns:
                features[col] = False
 
        if target_column is not None:
            self.valid_columns = features.columns
            target = pd.DataFrame(training_data[target_column])
            return features[self.features_cols], target

        return features[self.features_cols]

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """

        n_y0 = len(target[target == 0])
        n_y1 = len(target[target == 1])
        scale = n_y0/n_y1
        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        self._model.fit(features, target)
        self.fitted = True

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        print("PREDICTING!!!!!!!!!!!!!!!!!!!!!!!!!")
        return self._model.predict(features).astype(int).tolist()
    

def get_min_diff(data):
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds())/60
    return min_diff