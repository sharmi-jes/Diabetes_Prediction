import os
import sys
from Diabetetic.components.data_ingestion import DataIngestion
from Diabetetic.components.data_validation import DataValidation
from Diabetetic.components.data_transformation import DataTransformation
from Diabetetic.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
from Diabetetic.entity.artfact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
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

    logging.info("Data validation is started")
    data_validation_config=DataValidationConfig(training_pipeline)
    logging.info("data validation")
    data_validation=DataValidation(data_ingestion_artifacts,data_validation_config)
    logging.info("initaite the data validation")
    data_validation_artifacts=data_validation.initiate_data_validation()
    print(data_validation_artifacts)
    logging.info("complete the data validation")

    logging.info("data transformation is started")
    data_transformation_config=DataTransformationConfig(training_pipeline)
    logging.info("apply config to the data transformatin")
    data_transformation=DataTransformation(data_validation_artifacts,data_transformation_config)
    logging.info("call the iniate data transfrmation")
    data_transformation_artifact=data_transformation.initiate_data_transformation()
    print(data_transformation_artifact)
    logging.info("compledte the data transformation")


