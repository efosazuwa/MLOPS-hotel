import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path: str) -> dict:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in the given path: {file_path}")
        
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            logger.info(f"Successfully read the YAML file: {file_path}")
            return config
    
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise CustomException(f"Failed to read Yaml file", e)
    
def load_data(path: str):
    try:
        logger.info("loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading the  data: {e}")
        raise CustomException("failed to load data", e)