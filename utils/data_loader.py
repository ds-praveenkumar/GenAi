#===============================================================================
#  File Name    : dataLoader.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-07-21
#  Last Updated : 2025-07-21
#  Version      : v1.0.0

#  Language     : Python
#  File name    : dataLoader.py
#  Dependencies : 
#    - Dependency 1
#    - Dependency 2

#  Inputs       : Expected inputs
#  Outputs      : Expected outputs
#  Usage        : 
#    Example usage

#  Notes        : 
#    - Notes or TODOs
#===============================================================================
from datasets import load_dataset
from abc import ABC, abstractmethod


class BaseDataLoader(ABC):
    def __init__(self, data_path, dataset_name) :
        self.data_name = dataset_name
        self.data_path = data_path
    
    def load_data( self ):
        datasets = load_dataset(    
                                    self.data_name,
                                     self.data_path,
                                     trust_remote_code=True,)
        return datasets
    
class CSVDataLoader(BaseDataLoader):
    def __init__(self, data_path, dataset_name):
        super().__init__(data_path, dataset_name)
        
    def load_data( self , data_files = []):
        datasets = load_dataset( "csv",
                                trust_remote_code=True,
                                data_files=data_files)
        return datasets

class JSONDataLoader(BaseDataLoader):
    def __init__(self, data_path, dataset_name):
        super().__init__(data_path, dataset_name)
        
        
    def load_data(self, data_files = []):
        datasets = load_dataset(
                                "json",
                                data_files=data_files,
                                trust_remote_code=True)
        return datasets
    
