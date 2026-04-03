import os 
import sys
import numpy as np
import pandas as pd
import dill



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
  
  
