import os


# Data Ingestion

RAW_DIR = "artifacts/raw_data"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw_data.csv")

TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = "config/config.yaml"