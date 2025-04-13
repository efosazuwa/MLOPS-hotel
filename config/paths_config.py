import os


# Data Ingestion

RAW_DIR = "artifacts/raw_data"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw_data.csv")

TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = "config/config.yaml"


# DATA Processing
PROCESSED_DIR = 'artifacts/processed'
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")

# Model Training
MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl" 