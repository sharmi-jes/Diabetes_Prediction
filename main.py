import os
import sys
from Diabetetic.components.data_ingestion import DataIngestion
from Diabetetic.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from Diabetetic.entity.artfact_entity import DataIngestionArtifact
from Diabetetic.constants import trainingpipeline
from Diabetetic.exception import DiabeteticException
from Diabetetic.logging import logging

if __name__=="__main__":

    training_pipeline=TrainingPipelineConfig()
    data_ingestion_config=DataIngestionConfig(training_pipeline)

    logging.info("passed the data ingetion config to data ingestion class")

    data_ingestion=DataIngestion(data_ingestion_config)
    logging.info("completed the data ingestion and start the iniate data ingestion")
    data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifacts)

