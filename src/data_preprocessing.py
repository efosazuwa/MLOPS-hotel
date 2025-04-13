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

            random_state = self.config["data_processing"]["random_state"]
            smote = SMOTE(random_state=random_state)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Balanced data shape: ", extra={"balanced_data_shape": balanced_df.shape})
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error during balancing step: {e}")
            raise CustomException("Failed to balance data", e)
        
    def feature_selection(self, df: pd.DataFrame):
        try:
            logger.info("Starting feature selection step")

            X = df.drop(columns=['booking_status'])
            y = df["booking_status"]

            random_state = self.config["data_processing"]["random_state"]
            model = RandomForestClassifier(random_state=random_state)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                "feature": X.columns,
                "importance": feature_importance
            })
            feature_importance_df.sort_values(by="importance", ascending=False, inplace=True)

            num_features = self.config["data_processing"]["no_of_features"]
            top_features = feature_importance_df["feature"][:num_features].values
            logger.info("Top Features", extra={"top_features": top_features})

            target_variable = self.config["data_processing"]["target_column"]
            top_features_df = df[top_features.tolist() + [target_variable]]

            logger.info("Feature selection successful completed")
            return top_features_df

        except Exception as e:
            logger.error(f"Error during feature selection step: {e}")
            raise CustomException("Failed to select features data", e)
        

    def save_data(self, df: pd.DataFrame, file_path: str):
        try:
            logger.info(f"Saving data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved successfully to {file_path}")

        except Exception as e:
            logger.error(f"Error during saving data: {e}")
            raise CustomException("Failed to save data", e)
        
    def process_data(self):
        try:
            logger.info("Starting data processing pipeline")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing pipeline completed successfully")

        except Exception as e:
            logger.error(f"Error during processing pipeline: {e}")
            raise CustomException("Failed to complete processing pipeline", e)
        
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process_data()


