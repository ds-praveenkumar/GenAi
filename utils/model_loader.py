#===============================================================================
#  File Name    : model_loader.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-07-22
#  Last Updated : 2025-07-22
#  Version      : v1.0.0

#  Language     : Python
#  File name    : model_loader.py
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

from abc import ABC, abstractclassmethod
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

class BaseModelLoader():
    def __init__(self, model_id) -> None:
        self.model_id = model_id
        self.local_dir = "models/" + self.model_id.split('/')[-1]
        self.model = None
        self.tokenizer = True
        
    def load_model( self ):
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id,
                                                     cache_path = self.local_dir)
        return self.model
    
    def load_tokenizer( self ):
        self.tokenizer = AutoTokenizer.from_pretrained( self.model_id, 
                                                       cache_path = self.local_dir,
                                                       trust_remote_code = True,
                                                       use_fast=True
                                                       )
        return self.tokenizer
    
    def main( self ):
        model = self.load_model()
        tokenizer = self.load_tokenizer()
        return model, tokenizer
    
class BnBModelLoader(BaseModelLoader ):
    def __init__(self, model_id) -> None:
        self.model_id = model_id
        super().__init__(self.model_id)
        
        
    def get_bnb_config( self ):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit = True,
            bnb_4bit_use_double_quant = True,
            bnb_4bit_quant_type = "nf4",
            bnb_4bit_compute_dtype = torch.float16
        )
        return bnb_config
    
    def load_model(self):
        bnb_config = self.get_bnb_config()
        self.model =  AutoModelForCausalLM.from_pretrained(
                                                            self.model_id,
                                                            device_map="cuda",
                                                            use_cache=False,
                                                            attn_implementation="flash_attention_2",
                                                            torch_dtype=torch.bfloat16,
                                                            quantization_config=bnb_config,
                                                            
)
        return self.model
        
    def load_tokenizer( self ):
        self.tokenizer = AutoTokenizer.from_pretrained( self.model_id, 
                                                       cache_path = self.local_dir,
                                                       trust_remote_code = True,
                                                       use_fast=True,
                                                       device_map="cuda"
                                                       )
        return self.tokenizer
    
if __name__ == '__main__':
    model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    model_loader = BnBModelLoader(model_id=model_id)
    model = model_loader.load_model()
    tokenizer = model_loader.load_tokenizer()
    print(model)
    