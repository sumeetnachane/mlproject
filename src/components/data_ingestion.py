import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

# Where to save the data after ingestion
@dataclass ## dataclass ka use krne se hum apne class ke andar variables ko define kar sakte hai, jisse code clean aur efficient hota hai
class DataIngestionConfig:
  train_data_path: str=os.path.join('artifacts', "train.csv")
  test_data_path: str=os.path.join('artifacts', "test.csv")
  raw_data_path: str=os.path.join('artifacts', "data.csv") # initial data 

class DataIngestion:
  def __init__(self,):
    self.ingestion_config=DataIngestionConfig()

  def intiate_data_ingestion(self): 
    logging.info("Entered the data ingestion method or component")
    try:
      df=pd.read_csv("notebook\data\stud.csv")
      logging.info('Read the dataset as dataframe')

      os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True) ## iska use krne se directory create ho jayegi agar exist nahi karti hai to, exist_ok=True= aur exist karti hai to kuch nahi hoga

      df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True) # ye initial data ko bhi save karna chahte hai

      logging.info("Train test split initiated")
      train_set, test_set=train_test_split(df, test_size=0.2, random_state=42)

      train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

      test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

      logging.info("Ingestion of the data is completed")

      return(
        self.ingestion_config.train_data_path,
        self.ingestion_config.test_data_path
      )
    except Exception as e:
      raise CustomException(e, sys)

if __name__=="__main__":
  obj=DataIngestion()
  train_data,test_data = obj.intiate_data_ingestion()     

  data_transformation=DataTransformation()
  train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data, test_data) 

  modeltrainer = ModelTrainer()
  print(modeltrainer.initiate_model_trainer(train_arr, test_arr)) ## ye function best model ko return karega, jise hum future me use kar sakte hai prediction ke liye r2 score ke sath
      

