import os
import pandas as pd
import joblib
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