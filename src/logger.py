
import logging 
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" ## log file ka naam date aur time ke sath banega
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) ## logs folder ke andar log file create hoga
os.makedirs(logs_path,exist_ok=True) ## agar logs folder nahi hai to create kar dega


LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE) ## log file ka path


logging.basicConfig(
  filename=LOG_FILE_PATH, ## log file ka path
  format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", ## log message ka format
  level=logging.INFO,
)



if __name__=="__main__":
  logging.info("Logging has started")




# logger.py kya hota hai?
# Logging system setup karne ke liye file
# “Program me kya ho raha hai uska record rakhna”

# Simple language:
# Jab tumhara ML project run hota hai:
# kaun sa step start hua
# error kaha aaya
# data kaha save hua
# Ye sab console me print karne ke bajay log file me store hota hai

# error ko text file me store karna
