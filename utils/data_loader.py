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
    def __init__(self,  dataset_name) :
        self.data_name = dataset_name
        self.local_path = f'data/'
        self.datasets = None
    
    def load_data( self ):
        datasets = load_dataset(    
                                    self.data_name,
                                    trust_remote_code=True,
                                    cache_dir=self.local_path
                                     )
        self.datasets = datasets
        return self.datasets
    
    def show_examples( self , idx:int = 0):
        self.datasets = self.load_data()
        print(self.datasets['train'][idx])
    
class CSVDataLoader(BaseDataLoader):
    def __init__(self,  dataset_name):
        super().__init__(dataset_name)
        
    def load_data( self , data_files = []):
        datasets = load_dataset( "csv",
                                trust_remote_code=True,
                                data_files=data_files)
        return datasets

class JSONDataLoader(BaseDataLoader):
    def __init__(self, dataset_name):
        super().__init__( dataset_name)
        
        
    def load_data(self, data_files = []):
        datasets = load_dataset(
                                "json",
                                data_files=data_files,
                                trust_remote_code=True)
        return datasets
    
if __name__ == '__main__':
    DATA_NAME = "HuggingFaceH4/llava-instruct-mix-vsft"
    dl = BaseDataLoader(DATA_NAME)
    dl.show_examples(0)