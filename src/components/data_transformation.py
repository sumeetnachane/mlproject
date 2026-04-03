import subprocess
from dataclasses import dataclass
import sys

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer ## missing value ko handle krne ke liye
from sklearn.pipeline import Pipeline ## pipeline ka use krne se hum apne data transformation ke steps ko ek sath combine kar sakte hai, jisse code clean aur efficient hota hai

from sklearn.preprocessing import OneHotEncoder, StandardScaler ## categorical data ko numerical data me convert karne ke liye one hot encoding ka use karte hai, aur numerical data ko scale karne ke liye standard scaler ka use karte hai

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

# dataclass ka use krne se hum apne class ke andar variables ko define kar sakte hai, jisse code clean aur efficient hota hai
@dataclass 
class DataTransformationConfig:
  preprocessor_obj_file_path=os.path.join('artifacts', "preprocessor.pkl") ## ye file me hum apne preprocessor object ko save karenge, jisse hum future me use kar sakte hai

class DataTransformation:
  def __init__(self):
    self.data_transformation_config=DataTransformationConfig()


  def get_data_transformer_object(self):
    '''
    This function is responsible for data transformation based on the different types of data. It will handle both numerical and categorical data.
    '''
    try:
      numerical_columns = ["writing_score", "reading_score"] 
      categorical_columns = [
        "gender",
        "race_ethnicity",
        "parental_level_of_education",
        "lunch",
        "test_preparation_course",
      ]

      num_pipeline= Pipeline(
        steps=[
          ("imputer", SimpleImputer(strategy="median")), ## missing value ko median se fill karenge
          ("scaler", StandardScaler()) ## numerical data ko scale karenge
        ]
      )
      cat_pipeline=Pipeline(
        steps=[
          ("imputer", SimpleImputer(strategy="most_frequent")), ## missing value ko most frequent value se fill karenge
          ("one_hot_encoder", OneHotEncoder()),
          ("scaler", StandardScaler(with_mean=False)) ## categorical data ko scale karenge, with_mean=False isliye kyunki one hot encoding ke baad humare paas sparse matrix hota hai, jisme mean ko calculate karna possible nahi hota hai
        ]
      )  
      logging.info(f"Categorical columns: {categorical_columns}")

      logging.info(f"Numerical columns: {numerical_columns}")

      preprocessor=ColumnTransformer(
        [
          ("num_pipeline", num_pipeline, numerical_columns),
          ("cat_pipeline", cat_pipeline, categorical_columns)
          
        ]
      )

      return preprocessor
      
    except Exception as e:
      raise CustomException(e, logging)  


  def initiate_data_transformation(self, train_path, test_path):

    try:
      train_df=pd.read_csv(train_path)
      test_df=pd.read_csv(test_path)

      logging.info("Read train and test data completed.")

      logging.info("Obtaining preprocessing object.")

      preprocessing_obj=self.get_data_transformer_object()

      target_column_name="math_score"
      numerical_columns = ["writing_score", "reading_score"]

      input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)
      target_feature_train_df=train_df[target_column_name]

      input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
      target_feature_test_df=test_df[target_column_name]

      logging.info(
        f"Applying preprocessing object on training dataframe and testing dataframe."
      )

      input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
      input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

     # np.c_ ka use karne se hum apne input features aur target feature ko ek sath combine kar sakte hai, jisse hum apne model ko train kar sakte hai

      train_arr = np.c_[
        input_feature_train_arr, np.array(target_feature_train_df) 
      ]
      test_arr = np.c_[
        input_feature_test_arr, np.array(target_feature_test_df)  
      ]

      logging.info(f"Saved preprocessing object.")

      save_object(
        file_path=self.data_transformation_config.preprocessor_obj_file_path,
        obj=preprocessing_obj
      )

      return (
        train_arr,
        test_arr,
        self.data_transformation_config.preprocessor_obj_file_path
      )

      
    except Exception as e:
      raise CustomException(e, sys)
    


