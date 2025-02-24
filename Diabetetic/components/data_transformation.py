import os
import sys
import pandas as pd
import numpy as np
from Diabetetic.exception import DiabeteticException
from Diabetetic.logging import logging
from Diabetetic.constants import trainingpipeline
from Diabetetic.entity.artfact_entity import DataValidationArtifact,DataTransformationArtifact
from Diabetetic.entity.config_entity import DataTransformationConfig
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from Diabetetic.constants.trainingpipeline import TARGET_COLUMN
from Diabetetic.utils.main_utils.utils import save_numpy_array_data,save_object
one_encoder=OneHotEncoder()
scaler=StandardScaler()

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config

        except Exception as e:
            raise DiabeteticException(e,sys)
        
    logging.info("read the data from previous artuifact")
    def read_data(self,file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise DiabeteticException(e,sys)
        

    logging.info("create  preprocessor function")    
    def convert_data_numeric_and_scaler(self,df):
        try:
            # df=pd.read_csv(file_path)
            categorical_cols=df.select_dtypes(include="object").columns
            numerical_cols = df.select_dtypes(exclude="object").columns.drop("diabetes", errors="ignore")
            print(numerical_cols)
            # for col in categorical_cols.columns:
            #     col=categorical_cols[col]
            #     categorical_cols[col]=label_encoder.fit_transform(categorical_cols[col])
            
            # for col in df.columns:
            #     column=df[col]
            #     column=scaler.fit_transform(column)

            cat_pipeline=Pipeline(
                [
                    ("one_hot_encoder",OneHotEncoder(handle_unknown="ignore"))
                ]
            )
            num_pipeline=Pipeline(
                [
                    ("scaler",StandardScaler())
                ]
            )


            preprocessor=ColumnTransformer(
                [ 
                    ("cat_pipeline",cat_pipeline,categorical_cols),
                    ("num_pipeline",num_pipeline,numerical_cols)
                    
                ]
            )  

            return preprocessor
        except Exception as e:
            raise DiabeteticException(e,sys)
        
    def initiate_data_transformation(self):
        try:
            train_data=self.data_validation_artifact.valid_train_file_path
            test_data=self.data_validation_artifact.valid_test_file_path

            logging.info("read the data fundtion")
            train_df=self.read_data(train_data)
            test_df=self.read_data(test_data)
            print(train_df.head(2))
            print(test_df.head(2))

            logging.info('remove the target col from input  train data')
            train_input_data=train_df.drop(columns=TARGET_COLUMN)
            train_target_data=train_df[TARGET_COLUMN]

            logging.info('remove the target col from input  test data')
            test_input_data=test_df.drop(columns=TARGET_COLUMN)
            test_target_data=test_df[TARGET_COLUMN]

            logging.info("calling the preprocessor object")
            logging.info("Creating and fitting the preprocessor.")
            preprocessor = self.convert_data_numeric_and_scaler(train_df)
            preprocessor.fit(train_input_data)  # Fit only on training data

            # Transform train and test data
            logging.info("Transforming train and test data.")
            preprocessor_train_input_data = preprocessor.transform(train_input_data)
            preprocessor_test_input_data = preprocessor.transform(test_input_data)


            logging.info("combine the input data along with target col")
            train_arr=np.c_[
                preprocessor_train_input_data,train_target_data
            ]
            test_arr=np.c_[
                preprocessor_test_input_data,test_target_data
            ]


            logging.info("save the train and test arr in the form of numpy array data")
            save_numpy_array_data(self.data_transformation_config.data_transformed_train_file,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.data_transformed_test_file,array=test_arr)
            logging.info("save the preprocessor object")
            save_object(self.data_transformation_config.data_transformed_object,preprocessor)
            # save_object(self.data_transformation_config.data_transformed_object,preprocessor_test)

            data_transformation_artifact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file,
                transformed_test_file_path=self.data_transformation_config.data_transformed_test_file,
                transformed_object_dir=self.data_transformation_config.data_transformed_object
            )

            return data_transformation_artifact
        except Exception as e:
            raise DiabeteticException(e,sys)




         
