import os
import sys
import pymongo
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from Diabetetic.exception import DiabeteticException
from Diabetetic.logging import logging
from Diabetetic.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from Diabetetic.entity.artfact_entity import DataIngestionArtifact

# Load environment variables
load_dotenv()

# Get MongoDB URL from .env file
MONGO_DB_URL = os.getenv("MONGO_DB_URL") or "mongodb://localhost:27017"

logging.info("Initializing DataIngestion class")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise DiabeteticException(e, sys)

    logging.info("Reading data from MongoDB")

    def read_data_from_mongodb(self):
        try:
            database = self.data_ingestion_config.database_name
            collection = self.data_ingestion_config.collection_name

            logging.info(f"Connecting to MongoDB database: {database}, collection: {collection}")

            # Establish MongoDB connection
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database][collection]

            # Convert MongoDB collection to DataFrame
            df = pd.DataFrame(list(collection.find()))

            if df.empty:
                raise ValueError("MongoDB collection is empty. No data retrieved.")

            if "_id" in df.columns:
                df.drop(columns=['_id'], inplace=True)  # Drop MongoDB's _id column
            
            df.replace({"na": np.nan}, inplace=True)

            logging.info(f"Data fetched successfully from MongoDB: {df.shape}")

            return df  # 🔥 Fix: Ensure DataFrame is returned
        except Exception as e:
            raise DiabeteticException(e, sys)

    logging.info("Saving data to feature store path")

    def feature_store_path(self, dataframe: pd.DataFrame):
        try:
            if dataframe is None or dataframe.empty:
                raise ValueError("Received empty dataframe. Cannot save to CSV.")

            feature_store_path = self.data_ingestion_config.feature_store_path
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)

            dataframe.to_csv(feature_store_path, index=False)  # 🔥 Fix: Added index=False
            logging.info(f"Data saved to feature store path: {feature_store_path}")

            return dataframe
        except Exception as e:
            raise DiabeteticException(e, sys)

    logging.info("Splitting train and test data")

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.feature_plsit_ration, random_state=42
            )

            logging.info(f"Data split into train ({train_set.shape}) and test ({test_set.shape})")

            # Ensure directories exist
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_file_path), exist_ok=True)

            # Save train and test data
            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)

            logging.info("Train and test CSV files saved successfully.")

        except Exception as e:
            raise DiabeteticException(e, sys)

    logging.info("Starting data ingestion pipeline")

    def initiate_data_ingestion(self):
        try:
            # Read data from MongoDB
            dataframe = self.read_data_from_mongodb()

            if dataframe is None or dataframe.empty:
                raise ValueError("Data ingestion failed. No data received from MongoDB.")

            # Save to feature store
            dataframe = self.feature_store_path(dataframe)

            # Split data
            self.split_data_as_train_test(dataframe)

            # Create artifact
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            return data_ingestion_artifact
        except Exception as e:
            raise DiabeteticException(e, sys)

            


            


