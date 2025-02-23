import os
import sys
from Diabetetic.constants import trainingpipeline
import pandas as pd
import numpy as np
from Diabetetic.exception import DiabeteticException
from Diabetetic.logging import logging
from Diabetetic.entity.artfact_entity import DataIngestionArtifact,DataValidationArtifact
from Diabetetic.entity.config_entity import DataValidationConfig
from scipy.stats import ks_2samp
from Diabetetic.constants.trainingpipeline import SCHEMA_FILE_PATH
from Diabetetic.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_path=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise DiabeteticException(e,sys)
    logging.info("read the train and test data from artifact")    
    def read_data(self,file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise DiabeteticException(e,sys)
    logging.info("validate the number of cols in dataframe and schema path")    
    def validate_no_of_cols(self,dataframe:pd.DataFrame):
        try:
            schema_files=len(self.schema_path)
            data_frame_files=len(dataframe.columns)
            logging.info("take the both length of schema and df")
            if schema_files==data_frame_files:
                return True
            else:
                return False
        except Exception as e:
            raise DiabeteticException(e,sys)
        
    logging.info("detect drift path like compare the train and test distributions")

    def detect_drift_path(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for col in base_df.columns:
                d1=base_df[col]
                d2=current_df[col]
                is_samp_dist=ks_2samp(d1,d2)
                if threshold<=is_samp_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({col:{
                    "p_value":float(is_samp_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report) 

            # os.makedirs(dir_path,exist_ok=True)
            # write_yaml_file(file_path=dir_path,content=report)
        except Exception as e:
            raise DiabeteticException(e,sys)
        
    def count_no_of_numerical_cols(self,dataframe:pd.DataFrame):
        try:
            df=pd.read_csv(dataframe)
            count_numerical=df.select_dtypes(exclude="object").columns
            print(count_numerical)
            print(len(count_numerical))
        except Exception as e:
            raise DiabeteticException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info("read the train an dtest data from artifact ingestion folder")
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            logging.info("read the train data from the read function")
            train_data=self.read_data(train_file_path)
            test_data=self.read_data(test_file_path)

            logging.info("check validate number of cols")
            status=self.validate_no_of_cols(train_data)
            if not status:
                error_message=f"train data has not all cols {train_data}"
            
            status=self.validate_no_of_cols(test_data)
            if not status:
                error_message=f"train data has not all cols {test_data}"

            
            ## lets check datadrift
            status=self.detect_drift_path(base_df=train_data,current_df=test_data)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_data.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)

            test_data.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
   
            )



            return data_validation_artifact
        except Exception as e:
            raise DiabeteticException(e,sys)
            





        
            



            




