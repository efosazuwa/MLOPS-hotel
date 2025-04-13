import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import * 
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint

logger = get_logger(__name__)

class ModelTrainer:

    def __init__(self, train_path: str, test_path:str, model_output_path:str, config_path:str):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        
        self.config = read_yaml(config_path)

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path} and {self.test_path}")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            target_column = self.config["data_processing"]["target_column"]

            X_train = train_df.drop(columns=[target_column])
            y_train = train_df[target_column]
            X_test = test_df.drop(columns=[target_column])
            y_test = test_df[target_column]

            logger.info("Data loaded and split into features and target")

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error loading and splitting data: {e}")
            raise CustomException('Failed to load and split data', e)
        
    def train_model(self, X_train, y_train):
        try:
            logger.info("Initiallizing model")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting Randomized Search CV")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                **self.random_search_params
            )

            random_search.fit(X_train, y_train)

            logger.info('Random search complete')

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_
            
            logger.info(f"Best parameters found", extra={"best_params": best_params})

            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error while training model: {e}")
            raise CustomException('Failed to train model', e)
        
    def evaluate_model(self, model, X_test, y_test) -> dict:
        try:
            logger.info("Starting model evaluation")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Accuracy: {accuracy}", extra={"accuracy": accuracy})
            logger.info(f"Precision: {precision}", extra={"precision": precision})
            logger.info(f"recall: {recall}", extra={"recall": recall})
            logger.info(f"F1: {f1}", extra={"f1": f1})

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1
            }
        except Exception as e:
            logger.error(f"Error during model evaluation: {e}")
            raise CustomException('Failed to evaluate model', e)
        
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info(f"Saving model to {self.model_output_path}")
            joblib.dump(model, self.model_output_path)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error during model saving: {e}")
            raise CustomException('Failed to save model', e)
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting model training pipeline")
                logger.info("Starting MLFlow run")
                logger.info("Logging the training and testing dataset to MLFlow")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_lgbm_model = self.train_model(X_train, y_train)
                evaluation_metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)

                logger.info("Logging model to MLFlow")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging model params and metrics to MLFlow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(evaluation_metrics)

                logger.info("Model training pipeline completed successfully")

        except Exception as e:
            logger.error(f"Error during model training pipeline: {e}")
            raise CustomException('Failed to train model', e)
        
if __name__ == "__main__":
    model_trainer = ModelTrainer(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH, CONFIG_PATH)
    model_trainer.run()