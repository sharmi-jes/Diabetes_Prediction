import os
import sys
from Diabetetic.constants import trainingpipeline
import pandas as pd
import numpy as np
from Diabetetic.exception import DiabeteticException
from Diabetetic.logging import logging
from Diabetetic.entity.artfact_entity import DataIngestionArtifact,DataValidationArtifact
from Diabetetic.entity.config_entity import DataIngestionConfig
import os
import sys
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)


from pymongo import MongoClient

# MONGO_DB_URL = "your_mongodb_url"  # Update with actual MongoDB URL
DATABASE_NAME = "sharmianyum"  # Update with your database name
COLLECTION_NAME = "diabetic_data"  # Update with your collection name

client = MongoClient(MONGO_DB_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Check if MongoDB contains any records
count = collection.count_documents({})
print(f"Total records in MongoDB: {count}")

# Fetch a few records to inspect
sample_data = list(collection.find().limit(5))
for record in sample_data:
    print(record)
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from Diabetetic.exception import DiabeteticException

# class DataIngestion:
#     def __init__(self, db_collection):
#         self.db_collection = db_collection

#     def read_data_from_mongodb(self):
#         try:
#             # Fetch data from MongoDB
#             data = list(self.db_collection.find())
            
#             if not data:
#                 raise ValueError("MongoDB collection is empty. No data retrieved.")
            
#             df = pd.DataFrame(data)
            
#             if "_id" in df.columns:
#                 df.drop(columns=["_id"], inplace=True)
            
#             return df
#         except Exception as e:
#             raise DiabeteticException(e, sys)

#     def split_data_as_train_test(self, dataframe):
#         try:
#             if dataframe.empty:
#                 raise ValueError("The dataset is empty. Cannot split into train and test sets.")
            
#             train_set, test_set = train_test_split(
#                 dataframe, test_size=0.2, random_state=42
#             )
            
#             return train_set, test_set
#         except Exception as e:
#             raise DiabeteticException(e, sys)

#     def initiate_data_ingestion(self):
#         try:
#             dataframe = self.read_data_from_mongodb()
#             print(f"Total records in MongoDB: {len(dataframe)}")
            
#             if dataframe.empty:
#                 raise ValueError("No data available for ingestion.")
            
#             train_data, test_data = self.split_data_as_train_test(dataframe)
#             return train_data, test_data
#         except Exception as e:
#             raise DiabeteticException(e, sys)



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise DiabeteticException(e,sys)
        


        
    def export_collection_as_dataframe(self):
        """
        Read data from mongodb
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            print(len(df))
            return df
        except Exception as e:
            raise DiabeteticException(e,sys)
        
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            print(len(dataframe))
            return dataframe
        
            
        except Exception as e:
            raise DiabeteticException(e,sys)
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

            
        except Exception as e:
            raise DiabeteticException(e,sys)
        
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact

        except Exception as e:
            raise DiabeteticException(e,sys)

        
    




