from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTrainer

from utils.common_functions import read_yaml

from config.paths_config import *

if __name__=="__main__":
    # Data Ingestion

    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()

    # Data Processing

    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process_data()

    # Model Training

    model_trainer = ModelTrainer(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH, CONFIG_PATH)
    model_trainer.run()