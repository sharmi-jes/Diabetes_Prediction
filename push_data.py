import os
import sys
import pandas as pd
from Diabetetic.exception import DiabeteticException
from Diabetetic.logging import logging
import json
import pymongo


from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

'''Main aim of this code is to passed whole data to mongodb'''


logging.info("create a passed data class for passing adta to mongodb")
class PassedData:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise DiabeteticException(e,sys)
    logging.info("csv data format converted into jscon format")     
    def read_csv_to_json_format(self,filepath):
        try:
            df=pd.read_csv(filepath)
            df.reset_index(drop=True,inplace=True)
            print(df.head(2))
            records=list(json.loads(df.T.to_json()).values())
            print(records)
            return records
        except Exception as e:
            raise DiabeteticException(e,sys)
        
    logging.info("passed data to mongodb")
    def passed_data_to_mongodb(self,records,database,collection):
        try:
            self.records=records
            self.database=database
            self.collection=collection

            self.monog_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.monog_client[self.database]
            self.collection=self.database[self.collection]

            records=self.collection.insert_many(self.records)

            return records
        except Exception as e:
            raise DiabeteticException(e,sys)
        

if __name__=="__main__":
    file_path=r"D:\RESUME ML PROJECTS\Diabetes Prediction\notebooks\diabetes_prediction_dataset.csv"
    database="sharmianyum"
    collection="Diabetetic"
    data=PassedData()
    records=data.read_csv_to_json_format(file_path)
    no_of_records=data.passed_data_to_mongodb(records,database=database,collection=collection)
    print(no_of_records)


