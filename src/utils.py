import os 
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score



from src.exception import CustomException

def save_object(file_path, obj):
  try:
    dir_path = os.path.dirname(file_path)

    os.makedirs(dir_path, exist_ok=True)

    with open(file_path, "wb") as file_obj:
      dill.dump(obj, file_obj)
      ## dill ka use krne se hum apne object ko serialize kar sakte hai, jisse hum apne model ko save kar sakte hai aur future me use kar sakte hai, dump ka use krne se hum apne object ko file me save kar sakte hai, file_path me hum apne file ka path denge jaha hum apne model ko save karna chahte hai, obj me hum apne model ko denge jise hum save karna chahte hai

  except Exception as e:
    raise CustomException(e, sys)    
  

def evaluate_models(X_train, y_train, X_test, y_test, models):
    try:
      report = {}

      for i in range(len(list(models))):
        model = list(models.values())[i]

        model.fit(X_train, y_train) # Training the model

        y_train_pred = model.predict(X_train)

        y_test_pred = model.predict(X_test)

        train_model_score = r2_score(y_train, y_train_pred)

        test_model_score = r2_score(y_test, y_test_pred)

        report[list(models.keys())[i]] = test_model_score

      return report
    except Exception as e:
      raise CustomException(e, sys)
  
