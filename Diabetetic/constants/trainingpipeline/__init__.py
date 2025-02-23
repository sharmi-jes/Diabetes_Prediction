import os
import sys

'''TRAINING PIPELINE RELATED CONSTANT VARIABLES'''

TARGET_COLUMNS="diabetes"
ARTIFACT_DIR="Artifacts"
PIPELINE_NAME="Diabetetic"
FILE_NAME=r"D:\RESUME ML PROJECTS\Diabetes Prediction\diabetic_data\diabetes_prediction_dataset.csv"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

'''DATA INGETSION RELATED VARIABLES'''

DATA_INGESTION_ROOT_DIR="data_ingestion"
DAT_INGESTION_DIR="ingestion"
DATA_INGESTION_FEATURE_STORE="feature_store"
DATA_INGESTION_SPLIT_RATION=0.2
DATA_INGESTION_DATABASE_NAME="sharmianyum"
DATA_INGESTION_COLLECTION_NAME="diabetic_data"


"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"




