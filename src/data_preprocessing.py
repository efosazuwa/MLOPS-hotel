import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self, train_path: str, test_path: str, processed_dir: str, config_path: str):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config: dict = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            logger.info("Starting data preprocessing")

            logger.info("Dropping unnecessary columns and duplicates")

            drop_columns = self.config["data_processing"]["drop_columns"]
            df.drop(columns= drop_columns, inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            logger.info("Label Encoding")

            label_encoder = LabelEncoder()
            mappings = {}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}

            logger.info("Label Mappings", mappings)

            logger.info("Skewness Handling")
            skewness_threshold = self.config["data_processing"]["skew_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness> skewness_threshold].index:
                df[column] = np.log1p(df[column])

            return df
        
        except Exception as e:
            logger.error(f"Error during data preprocessing: {e}")
            raise CustomException("Failed to preprocess data", e)
        
    def balance_data(self, df: pd.DataFrame):
        try:
            logger.info("Handling Imbalanced data")
            X = df.drop(columns=['booking_status'])
            y = df["booking_status"]

            smote = SMOTE(random_state=30)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Balanced data shape: ", balanced_df.shape)
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error during balancing step: {e}")
            raise CustomException("Failed to balancee data", e)