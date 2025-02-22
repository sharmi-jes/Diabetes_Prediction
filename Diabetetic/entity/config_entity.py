import os
import sys
from Diabetetic.exception import DiabeteticException
from Diabetetic.logging import logging

from Diabetetic.constants import trainingpipeline
from datetime import datetime


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=trainingpipeline.PIPELINE_NAME
        self.artifact_name=trainingpipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestamp: str=timestamp


logging.info("create the dataingestionconfig class")
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_root_dir=os.path.join(training_pipeline_config.artifact_dir,trainingpipeline.DATA_INGESTION_ROOT_DIR)
        self.data_ingestion_dir=os.path.join(self.data_ingestion_root_dir,trainingpipeline.DAT_INGESTION_DIR)
        self.feature_store_path=os.path.join(self.data_ingestion_root_dir,trainingpipeline.DATA_INGESTION_FEATURE_STORE)
        self.train_file_path=os.path.join(self.data_ingestion_root_dir,trainingpipeline.TRAIN_FILE_NAME)
        self.test_file_path=os.path.join(self.data_ingestion_root_dir,trainingpipeline.TEST_FILE_NAME)
        self.feature_plsit_ration=trainingpipeline.DATA_INGESTION_SPLIT_RATION
        self.database_name=trainingpipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name=trainingpipeline.DATA_INGESTION_COLLECTION_NAME
