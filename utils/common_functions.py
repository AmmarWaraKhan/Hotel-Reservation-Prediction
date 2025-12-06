import os
import pandas 
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml
import pandas as pd

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {file_path} read successfully.")
            return config
    
    except Exception as e:
        logger.error(f"Error while reading YAML file: {e}")
        raise CustomException("Failed to read YAML file",e)
    
    
    
def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading data {e}")
        raise CustomException("Failed loading data", e)
    
    
        
    
            
            
        
    
